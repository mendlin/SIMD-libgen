#!/home/linmengl/.rvm/rubies/ruby-1.9.3-p327/bin/ruby

# Translate Cpp header files to C
# Change IDISA calling signatures like esimd<8>::mergel into esimd_mergel_8

# Opt parse, run me with `./cpp2c.rb -h` to see help
require 'optparse'

options = {:del_origin => false}
OptionParser.new do |opts|
	opts.banner = "Translate Cpp header files to C\nUsage: cpp2c.rb cpp_file [options]"

	opts.on("-v", "--[no-]version", "Show version") do
		puts "cpp2c.rb, Ver 1.0. By Meng Lin"
	end

	opts.on("-o", "--output [OutFile]", String, "Output file") do |o_file|
		options[:output] = o_file
	end

	opts.on("-d", "--delete", "Delete original file [Default: NO]") do 
		options[:del_origin] = true
	end

	opts.on_tail("-h", "--help", "Show this message") do
		puts opts
		exit
	end
end.parse!

if ARGV.size != 1
	puts "Wrong arguments, run with -h to see help info."
	exit
end

options[:input] = ARGV[0]

unless options.has_key? :output
	t = options[:input].gsub(/\.hpp/, ".h").gsub(/\.cpp/, ".c")
	if t == options[:input]
		t << ".c"
	end
	options[:output] = t
end

puts "Running with #{options.inspect}"

# Function Class

class LineStore
	@@store = ""
	def self.get_code
		@@store	
	end

	def self.store_line line
		@@store += line

		# line stored, return a empty line
		"<empty>"
	end

	def self.dump
		return "" if @@store =~ /^[\s\n]*$/

		res = "#if (BLOCK_SIZE == 128) \n"
		res += @@store.gsub(/(?<=\{\{\{)BLOCK_SIZE\b/, "128")
		res += "#else\n"
		res += @@store.gsub(/(?<=\{\{\{)BLOCK_SIZE\b/, "256")
		res += "#endif\n"

		@@store = ""
		res
	end
end

class LineTranslator
	def self.t_once line
		if line =~ /^\#/
			line.gsub!(/_HPP/, "_H")
			line.gsub!("idisa.hpp", "idisa128_c.h")
			line.gsub!("idisa128.hpp", "idisa128_c.h")
			line.gsub!(/.hpp\"/, ".h\"")
		end

		# format_2: opPattern = 0
		# 	class_name<fw>::op(data_type arg, ...)
		f2 = /(simd\d*|hsimd\d*|esimd\d*|mvmd\d*|bitblock\d*)\<([^>]*)\>::(\w*)\(/
		m = line.match f2
		if m
			calling = "#{m[1]}_#{m[3]}_{{{#{m[2]}}}}("
			line.gsub!(m[0], calling)
		end

		# format_3: opPattern = 1
		# 	class_name<fw>::op<x>(data_type arg, ...)		
		f3 = /(simd\d*|hsimd\d*|esimd\d*|mvmd\d*|bitblock\d*)\<([^>]*)\>::(\w*)\<([^>]*)\>\(/
		m = line.match f3
		if m
			calling = "#{m[1]}_#{m[3]}_{{{#{m[2]}}}}(#{m[4]}, "
			line.gsub! m[0], calling
		end

		# format_4: opPattern = 3
		# 	class_name::op(data_type arg, ...)
		f4 = /(bitblock\d*)::(\w*)\(/
		m = line.match f4
		if m
			calling = "#{m[1]}_#{m[2]}("
			line.gsub! m[0], calling
		end

		# format_5: opPattern = 4
		# 	class_name::op<x>(data_type arg, ...)		
		f5 = /(bitblock\d*)::(\w*)\<([^>]*)\>\(/
		m = line.match f5
		if m
			calling = "#{m[1]}_#{m[2]}(#{m[3]}, "
			line.gsub! m[0], calling
		end

		# remove redundant comma, e.g. simd_op(, 1) into simd_op(1)
		line.gsub! /(?<=\(),\s(?=\w+)/, ""
		# cont. bitblock_srli(sh, ) into bitlblock_srli()
		line.gsub! /(?<=[\s\w]),\s+(?=\))/, ""

		# Another hack here. simd128 class is basically simd in IDISA C
		line.gsub! /\b(simd|hsimd|mvmd|esimd)128/, "\\1"

		line
	end

	def self.t line		
		begin
			last = line.clone
			line = self.t_once line
		end while last != line

		if line =~ /\{\{\{BLOCK_SIZE\b/
			LineStore.store_line line			
		else 
			dump = LineStore.dump			
			dump + line
		end		
	end
end

# Translation Starts here

begin
	outfile = File.new(options[:output], "w")
	outfile.puts("/* Generated by cpp2c.rb from #{options[:input]} \n * Use IDISA C support \n*/\n\n")

	File.open(options[:input], "r") do |infile|
		while (line = infile.gets)
			newline = LineTranslator.t line
			outfile.puts(newline) if newline != "<empty>"
		end
	end
	outfile.puts(LineStore.dump) # Dump still stored code lines
	outfile.close

	if options[:del_origin]
		puts `rm #{options[:input]}`  	
	end
rescue => err
	puts "Exception: #{err}"
	err
end
