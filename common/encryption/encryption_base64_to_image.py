import base64
import pytesseract
from PIL import Image


def base64_to_img(bstr, file_path):
    imgdata = base64.b64decode(bstr)
    file = open(file_path, 'wb')
    file.write(imgdata)
    file.close()


def base64_to_str(bstr):
    return base64.b64encode(bstr.encode("utf-8")).decode('utf-8')


def base64_to_text(file_path):
    text = pytesseract.image_to_string(Image.open(file_path))
    return text


if __name__ == '__main__':
    data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAAAyCAIAAACWMwO2AAAR/0lEQVR42u3cefhU1X3HcdwVFBEUEDTIjiCbCi4oyiIgKoIgywMIouyKCiiKAiqgrAqyPAgqi4CIsu+C2CVp2qRNmqgNVesSrSTVpk3apGldnr7Cca6HO5MfCj9wfjrfP+a5c+fMuefe857P9/O9984t9Rf7x19m4q8y8ddRfD8TP8jE30Txw0z8bSb+LoofZeLHmfj7TPxDFD/JxE+j+McofpaJn2fi1Shey8TrmfinKH6RiT2Z+OdMvBHFm5l4KxP/EsXbmXgninejeC8Tv8zE+1F8kIl/zcSHmdgbxa8y8etM/FsUH2Xi40z8exS/ycR/RPGfUfw2E7/LxH9l4r+j+H0m/pCJ/4nij5n430z8XxSlclKVE6zvR5EN1g+jyAbrR1EcClg/iyIbrNeiyAbrF1EcPrDeiyIbrA+iOExg/SaKnGD9NorDBNYnn3xSqmi5ygnWD6IoQq5ygvXjKLLB+kkURYP18yiKkKucYO2JIhusN6PIBuvtKIoG65dRFCFXOcH6VRTZYH0UxaGA9bsossH6fRTZYP0xiiMN1lfMgznB+un+cbjzYE6w3oriCOTBnGD9Oooi5ConWAeRB3OC9YcoipCrrwdWwWAVDNZBGKz9wCoYrILBKi6DlRusgsEqGKxDNFiHEayCwfouG6wDgFUwWAWDdXAG60uwCgarYLCK0WDlAKtgsAoG69AN1uECq2CwDsVgGZLN+Yo2qLKmxBmsosAqGKwjb7AsL1++vF+/fh07duzZs2efPn0mTZq0bNkyQ9JbkK4SYbC+AKtgsPLEYG3ZsmXMmDFVq1Y9+uijS5cufcwxx5QrV+7YY48966yzmjVrNmXKFNOBLS3z3GClwSoYrG/WYDVu3HjDhg1IKpUVRx11VNmyZb1eeeWV999/v8NIwPLWYB0WsAoG6+AMlhFKf927dy9VZMAOXscff3y1atUGDx6cnwbr008/LVUwWF83D3pro8VusHTy3HPPnXDCCQlDEiKAjt4XOTWsSZMm+Wmw/gTWt8xg+cgYdLVr1y6vhp3gddBgbd26NVAV9t1H2nvVZ/GewVq1alXCDV/VpUuXli1btm/fnjgdd9xxIANTDFabNm3y02DtB1ZJN1jC25deeonJnTp1aufOne+8884RI0YsXbrU3vnoIAyWvbjpppsY6p07d7Zq1apv376LFi0aOnToQw895FON0QYsy4dosMLy/PnzE24uuOCCCRMmTJ8+nTT67rp16+66667q1auTNAIWCLvxxhvz02AVP1jfoMEynu3bt999991NmzY999xzWd1KlSpVqVLlqquuGj169IoVK766wTIYB0GHEydOtN2VK1fedttt27ZtI10jR44031CbPHmyHkJmhJ2DIJEZQKAKcEXnQW9t14IGwArrH3300QSsBg0a3HfffRs3bgxnsMIJLW127NhhMHXr1oXXoEGD8tNg5QarBBksLfXmu5bnzZvXrl27OnXqsLcK9aP2haN/yimnwIt6bd682d6hIaRFrznB0mbt2rVwwRDlu/zyy8877zz5CKa6bd269a233qo3pdnChQu13LRp0+23316mTBnadssttxgwGsiko6ErxyEBC0OYs1374pCuXr3a70Gz5NQokhKwypcvf88992iQfWo0vHXo9J+fBusAYOWnwQrrdSLrPfDAA1wIQfI77tChQ5Ijsn2uROb3LZEBS34BhMLeyFFlpwwjiJ81zz//vAFQBWCp7e+44w4MoerUU0/FaP369Zs3b16vXj3SCC/LDz/88PDhw08++eRGjRpdfPHFFStWvPnmm22uatWq48ePnzNnjvIoqGCiqYSwX79+Dz74oARnJAlYtnXiiScm1Z+9I2kl6xJhGqwSYbB80TSY5m7duskFzCwJAZOqm4qE0zxBpbLLKC1r1qw5Y8YMgiG1LV++vH///hQCFjqkTI8//vjs2bM1kNdYKJN69dVXX3TRRZ06ddLbMftCP/Dl23ADmrlz5zZr1oxcde/e3XZpDLwsgI9DKleuHPJARngkYvTbHFUjnyQQfwMGDNCJn4QEhypYoxmOyZivv/56rmvNmjW4LCmXCA8LWIfbYNk6GkxerEzMLFN1+umnW+NXfv7555v7nj17mryUeplv/lefujKe3r17y1wdO3asXbt2rVq1VGEmu23btrTEjLZo0eKkk07SM3x1G5PqowsvvFBOXLBggTpOP75uvcIt6E3p0qUN0oJmejCeG2644eyzz+b8KleurCstja1GjRo4U70SUWBRUCAadrKhChUqaGNUOpTliR99zfNLhJ9molTJMli0IaVGQZ9YHGSQH8PesmWLLNmjRw811GmnnZa0bNiwIcPE/ZjI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"
    # data = "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,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"
    # data = "data:image/png;base64,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"
    # data = "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,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"
    # base64_to_img(data.split(",")[1], "../image/original_c.xlsx")
    # base64_to_img(data.split(",")[1], "../image/original.gif")
    base64_to_img(data.split(",")[1], "../../image/origina388l.png")
    # res = base64_to_str(data.split(",")[1])
    # result = run(data.split(",")[1], "../test_d/2.png")
    # print(base64_to_text("../test_d/3.png"))
    # print(res)