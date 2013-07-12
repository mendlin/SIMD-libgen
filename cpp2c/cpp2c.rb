#!/home/linmengl/.rvm/rubies/ruby-1.9.3-p327/bin/ruby

# Translate Cpp header files to C
# Change IDISA calling signatures like esimd<8>::mergel into esimd_mergel_8
# Ruby version 1.9.3

# Opt parse, run me with `ruby cpp2c.rb -h` to see help
require 'optparse'

options = {:del_origin => false}
OptionParser.new do |opts|
	opts.banner = "Translate Cpp header files to C\nUsage: cpp2c.rb cpp_file [options]"

	opts.on("-v", "--[no-]version", "Show version") do
		puts "cpp2c.rb, Ver 1.0. By Meng Lin"
		exit
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

# Translation Starts here

require_relative 'passes'
passes = [SharpPass.new, IDISAPass.new,
			ConditionWrapPass.new("BLOCK_SIZE", [128, 256]),
			ConditionWrapPass.new("FW", [8, 32]), 
			ConditionWrapPass1.new("sizeof(scanfield_t)", [1,2,4,8]),
			EvaluationPass.new]

passes.each	do |pass|
	pass.translate options
	options[:input] = options[:output]
end

if options[:del_origin]
	puts `rm #{options[:input]}`  	
end
