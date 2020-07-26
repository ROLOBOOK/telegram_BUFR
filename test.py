from processing_for_cron import *

def get_text_from_bufr(file):
    decoder = Decoder()
    with open(file, 'rb') as ins: # return text
        bufr_message = decoder.process(ins.read())
            # декодируем телеграмму в текстовый файл
    return NestedTextRenderer().render(bufr_message)


#list_ =  main(days=4, doubl=0, solo_file=0, add_in_bd=0, find_file='22008')
#list_file = main(days=1, doubl=0, solo_file=0, add_in_bd=0, find_file='31369')
#s = main(add_in_bd=0, doubl=0)
file = './0000/89611_20200724000000_IUK.bin'
f = './0000/70361_20200724230104_IUK.bin:'
path = '/home/bufr/aero_bufr/res2/2020/07/24'
s = main(days=1, doubl=0, solo_file=f, add_in_bd=0, find_file=0)
