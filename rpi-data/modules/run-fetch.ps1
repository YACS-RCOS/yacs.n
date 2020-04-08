# need to set terminal output to utf8
# https://stackoverflow.com/questions/40098771/changing-powershells-default-output-encoding-to-utf-8
# https://stackoverflow.com/questions/5326304/powershell-get-default-system-encoding
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
python "./fetch-course-info.py"