import os

import comtypes.client
from docxtpl import DocxTemplate

tmp_path = r"C:\Users\12074\Desktop\测试\tmp_word-原始.docx"
child_path = r"C:\Users\12074\Desktop\测试\full_csv_table0-副本.docx"
# child_path = r"C:\Users\12074\Desktop\测试\full_csv_table0.docx"
save_path = r"C:\Users\12074\Desktop\测试\tmp_word-存储.docx"

tmp = DocxTemplate(tmp_path)

# child_doc = tmp.new_subdoc(child_path)
# print(type(child_doc))

# 和 new_subdoc()通理
# sub = Subdoc(tmp,docpath=child_path)
# print(type(sub))

child_doc = DocxTemplate(child_path)
print(type(child_doc))
# # 渲染模板（这里的context可以为空，因为我们只是为了获取渲染后的XML，不需要具体的数据）
child_doc.render({})
print(type(child_doc))
# # 获取渲染后的XML
rendered_xml = child_doc.get_xml()
print(type(rendered_xml))

key_context = {'full_csv_0': rendered_xml}
tmp.render(key_context)

tmp.save(save_path)

pdf_file = os.path.join(r"C:\Users\12074\Desktop\测试" ,os.path.basename(save_path).replace('.docx', '.pdf'))
# 打开word应用程序
word = comtypes.client.CreateObject('Word.Application')
# 打开指定word文件
doc = word.Documents.Open(save_path)
# 保存并转换为pdf文档
doc.SaveAs(pdf_file, FileFormat=17)
# 关闭文档
doc.Close()
# 退出word
word.Quit()
