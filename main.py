import secrets

from PIL import Image
from fpdf import FPDF, HTMLMixin
import qrcode


class PDF(FPDF, HTMLMixin):
    pass


document = PDF()
document.add_page()
document.set_font('helvetica', size=12)

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!()=?{[]}'
head = ['ABC', 'DEF', 'GHI', 'JKL', 'MNO', 'PQR', 'STU', 'VWX', 'YZ1', '234']


def random_string():
    return secrets.choice(alphabet) + secrets.choice(alphabet) + secrets.choice(alphabet)


def generate_password_card():
    pc = []
    for row in range(10):
        row = []
        for col in range(10):
            row.append(random_string())
        pc.append(row)
    return pc


def save_pc(filename, pc):
    to_save = ''
    for row in range(len(pc)):
        for col in range(len(pc)):
            to_save += pc[row][col]
        if row != len(range(len(pc))) - 1:
            to_save += '\n'
    with open(filename, 'w') as out:
        out.write(to_save)


def load_pc(filename):
    pc = []
    with open(filename, 'r') as pc_in:
        for row in pc_in:
            row = row.strip()
            pc.append([row[0 + i:3 + i] for i in range(0, len(row), 3)])
    return pc


def pc_to_qr(filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )
    str = ""
    with open(filename, 'r') as pc_in:
        for row in pc_in:
            str += row
    qr.add_data(str)
    qr.make(fit=True)
    img = qr.make_image()
    type(img)
    img.save("qr.png")


def write_pdf():
    pc = load_pc("pc.txt")
    pc_to_qr("pc.txt")
    print(pc)
    width = int(100 / (float(len(head)) + 1.0))
    html_table = '<h1>PW Card</h1>\n<table border="1"><thead>\n<tr>\n'
    html_table += '<th width="' + str(width) + '%"> Counter </th>\n'
    for th in head:
        html_table += '<th width="' + str(width) + '%">' + th + '</th>\n'
    html_table += '</tr>\n</thead><tbody>'
    i = 1
    for row in range(len(pc)):
        if i % 2:
            html_table += '<tr bgcolor=#22FF22">'
        else:
            html_table += '<tr bgcolor=#DDFFDD">'
        html_table += '<td>' + str(i) + '</td>\n'
        i += 1
        for col in range(len(pc)):
            html_table += '<td>' + pc[row][col] + '</td>\n'
        html_table += '</tr>'
    html_table += '</tbody></table>'

    print(html_table)

    document.write_html(html_table)
    img = Image.open("./qr.png")
    img = img.resize((200, 200), resample=Image.NEAREST)
    document.image(img)

    document.output("card.pdf")


save_pc("pc.txt", generate_password_card())
write_pdf()
