
import subprocess

def katex(in_str):
	proc = subprocess.Popen(['katex'], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
	outs, errs = proc.communicate(input = in_str.encode('utf-8'))
	return outs.decode('utf-8')
