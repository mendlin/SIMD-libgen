class BasePass	
	def t line
		line
	end

	def output_header outfile, options
	end

	def output_tail outfile, options
	end

	def translate options
		infile_buff = []
		File.open(options[:input], "r") do |infile|			
			while (line = infile.gets)
				infile_buff << line 
			end
		end

		File.open(options[:output], "w") do |outfile|			
			output_header outfile, options

			for line in infile_buff
				newline = self.t line
				outfile.puts(newline) if newline != "<empty>"
			end			
			
			output_tail outfile, options
		end

		if options[:del_origin]
			puts `rm #{options[:input]}`  	
		end		
	end
end

# Add some info in the header of output
class OutputInfoPass < BasePass
	def output_header outfile, options
		outfile.puts "/* GENERATED CODE, DON'T MODIFY."
 		outfile.puts " * Use IDISA C support, by cpp2c.rb */"
 		outfile.puts ""
	end
end

# Port IDISA calls
# e.g 
#	simd<64>::add(a, b) => simd_add_{{{64}}}(a, b)
# 	simd<64>::srli<63>(a) => simd_srli_{{{64}}}(63, a)
#   esimd<BLOCK_SIZE/2>::mergel => esimd_mergel_{{{BLOCK_SIZE/2}}}
class IDISAPass < BasePass	
	def basic_t line
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

	def t line
		begin
			last = line.clone
			line = self.basic_t line
		end while last != line
		line
	end
end

# Port all cpp lines started with '#', like '#include', '#ifndef'
class SharpPass < BasePass
	def t line
		if line =~ /^\#/
			line.gsub!(/_HPP/, "_H")
			line.gsub!("idisa.hpp", "idisa128_c.h")
			line.gsub!("idisa128.hpp", "idisa128_c.h")
			line.gsub!(/.hpp\"/, ".h\"")
		end

		line
	end
end

# use #if #else #end to wrap KEYs as field width
# e.g. 
#   #define Carry0 simd<BLOCK_SIZE>::constant<0>()
#   #define Carry1 simd<BLOCK_SIZE>::constant<1>()
# After this pass, will become:
# 	#if (BLOCK_SIZE == 128) 
# 	    #define Carry0 simd_constant_128(0)
# 	    #define Carry1 simd_constant_128(1)
# 	#else
# 	    #define Carry0 simd_constant_256(0)
# 	    #define Carry1 simd_constant_256(1)
# 	#endif
class ConditionWrapPass < BasePass
	# e.g. key = "BLOCK_SIZE", values = [128, 256]
	def initialize key, values		
		@key = key
		@reg_key = Regexp.escape(key)
		@values = values
	end

	def output_header outfile, options
		@line_store = ""
	end

	def dump
		return "" if @line_store == ""

		res = ""		
		@values.each_with_index do |v, i|  
			if i == 0
				res += "#if (#{@key} == #{v}) \n"
			elsif i == @values.size - 1
				res += "#else //#{@key} == #{v}\n"
			else
				res += "#elif (#{@key} == #{v})\n"
			end

			res += @line_store.gsub /(\{\{\{[^}]*)#{@reg_key}/, "\\1#{v}"
		end
		res += "#endif\n"

		@line_store = ""
		res
	end

	def output_tail outfile, options		
		res = dump
		outfile.puts res if res != ""
	end

	def t line
		if line =~ /\{\{\{.*#{@reg_key}/
			@line_store += line
			"<empty>"
		else
			dump + line
		end
	end	
end

# Slightly different wrap, use "if" insted of "#if"
# In order to enable "sizeof()" as wrap condition
class ConditionWrapPass1 < ConditionWrapPass
	def dump
		return "" if @line_store == ""

		res = ""		
		@values.each_with_index do |v, i|  
			if i == 0
				res += "if (#{@key} == #{v}) {\n"
			elsif i == @values.size - 1
				res += "} else { //#{@key} == #{v}\n"
			else
				res += "} else if (#{@key} == #{v}) {\n"
			end

			res += @line_store.gsub /(\{\{\{[^}]*)#{@reg_key}/, "\\1#{v}"
		end
		res += "}\n"

		@line_store = ""
		res
	end
end

# Eval expressions inside {{{ }}}
# e.g. {{{256 / 2}}} => 128
class EvaluationPass < BasePass
	def t line
		# Eval all the math inside {{{ }}}, I LOVE RUBY!!!!
		line.gsub(/\{\{\{([^\{\}]*)\}\}\}/) { eval($1) }
	end
end