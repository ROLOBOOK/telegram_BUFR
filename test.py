from processing_for_cron import *

def get_text_from_bufr(file):
    decoder = Decoder()
    with open(file, 'rb') as ins: # return text
        bufr_message = decoder.process(ins.read())
            # декодируем телеграмму в текстовый файл
    return NestedTextRenderer().render(bufr_message)


#list_ =  main(days=4, doubl=0, solo_file=0, add_in_bd=0, find_file='22008')
#list_file = main(days=1, doubl=0, solo_file=0, add_in_bd=0, find_file='31369')
#f = './0000/24908_20200731233017_IUK.bin'
s = main(add_in_bd=0)

