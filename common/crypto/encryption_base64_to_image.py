import base64

import pytesseract
from PIL import Image


def base64_to_img(byte_str, file_path):
	imgdata = base64.b64decode(byte_str)
	with open(file_path, 'wb') as f:
		f.write(imgdata)


def base64_to_str(byte_str):
	return base64.b64encode(byte_str.encode("utf-8")).decode('utf-8')


def base64_to_text(file_path):
	return pytesseract.image_to_string(Image.open(file_path))


if __name__ == '__main__':
	data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAAAyCAIAAACWMwO2AAAR/0lEQVR42u3cefhU1X3HcdwVFBEUEDTIjiCbCi4oyiIgKoIgywMIouyKCiiKAiqgrAqyPAgqi4CIsu+C2CVp2qRNmqgNVesSrSTVpk3apGldnr7Cca6HO5MfCj9wfjrfP+a5c+fMuefe857P9/O9984t9Rf7x19m4q8y8ddRfD8TP8jE30Txw0z8bSb+LoofZeLHmfj7TPxDFD/JxE+j+McofpaJn2fi1Shey8TrmfinKH6RiT2Z+OdMvBHFm5l4KxP/EsXbmXgninejeC8Tv8zE+1F8kIl/zcSHmdgbxa8y8etM/FsUH2Xi40z8exS/ycR/RPGfUfw2E7/LxH9l4r+j+H0m/pCJ/4nij5n430z8XxSlclKVE6zvR5EN1g+jyAbrR1EcClg/iyIbrNeiyAbrF1EcPrDeiyIbrA+iOExg/SaKnGD9NorDBNYnn3xSqmi5ygnWD6IoQq5ygvXjKLLB+kkURYP18yiKkKucYO2JIhusN6PIBuvtKIoG65dRFCFXOcH6VRTZYH0UxaGA9bsossH6fRTZYP0xiiMN1lfMgznB+un+cbjzYE6w3oriCOTBnGD9Oooi5ConWAeRB3OC9YcoipCrrwdWwWAVDNZBGKz9wCoYrILBKi6DlRusgsEqGKxDNFiHEayCwfouG6wDgFUwWAWDdXAG60uwCgarYLCK0WDlAKtgsAoG69AN1uECq2CwDsVgGZLN+Yo2qLKmxBmsosAqGKwjb7AsL1++vF+/fh07duzZs2efPn0mTZq0bNkyQ9JbkK4SYbC+AKtgsPLEYG3ZsmXMmDFVq1Y9+uijS5cufcwxx5QrV+7YY48966yzmjVrNmXKFNOBLS3z3GClwSoYrG/WYDVu3HjDhg1IKpUVRx11VNmyZb1eeeWV999/v8NIwPLWYB0WsAoG6+AMlhFKf927dy9VZMAOXscff3y1atUGDx6cnwbr008/LVUwWF83D3pro8VusHTy3HPPnXDCCQlDEiKAjt4XOTWsSZMm+Wmw/gTWt8xg+cgYdLVr1y6vhp3gddBgbd26NVAV9t1H2nvVZ/GewVq1alXCDV/VpUuXli1btm/fnjgdd9xxIANTDFabNm3y02DtB1ZJN1jC25deeonJnTp1aufOne+8884RI0YsXbrU3vnoIAyWvbjpppsY6p07d7Zq1apv376LFi0aOnToQw895FON0QYsy4dosMLy/PnzE24uuOCCCRMmTJ8+nTT67rp16+66667q1auTNAIWCLvxxhvz02AVP1jfoMEynu3bt999991NmzY999xzWd1KlSpVqVLlqquuGj169IoVK766wTIYB0GHEydOtN2VK1fedttt27ZtI10jR44031CbPHmyHkJmhJ2DIJEZQKAKcEXnQW9t14IGwArrH3300QSsBg0a3HfffRs3bgxnsMIJLW127NhhMHXr1oXXoEGD8tNg5QarBBksLfXmu5bnzZvXrl27OnXqsLcK9aP2haN/yimnwIt6bd682d6hIaRFrznB0mbt2rVwwRDlu/zyy8877zz5CKa6bd269a233qo3pdnChQu13LRp0+23316mTBnadssttxgwGsiko6ErxyEBC0OYs1374pCuXr3a70Gz5NQokhKwypcvf88992iQfWo0vHXo9J+fBusAYOWnwQrrdSLrPfDAA1wIQfI77tChQ5Ijsn2uROb3LZEBS34BhMLeyFFlpwwjiJ81zz//vAFQBWCp7e+44w4MoerUU0/FaP369Zs3b16vXj3SCC/LDz/88PDhw08++eRGjRpdfPHFFStWvPnmm22uatWq48ePnzNnjvIoqGCiqYSwX79+Dz74oARnJAlYtnXiiScm1Z+9I2kl6xJhGqwSYbB80TSY5m7duskFzCwJAZOqm4qE0zxBpbLLKC1r1qw5Y8YMgiG1LV++vH///hQCFjqkTI8//vjs2bM1kNdYKJN69dVXX3TRRZ06ddLbMftCP/Dl23ADmrlz5zZr1oxcde/e3XZpDLwsgI9DKleuHPJARngkYvTbHFUjnyQQfwMGDNCJn4QEhypYoxmOyZivv/56rmvNmjW4LCmXCA8LWIfbYNk6GkxerEzMLFN1+umnW+NXfv7555v7nj17mryUeplv/lefujKe3r17y1wdO3asXbt2rVq1VGEmu23btrTEjLZo0eKkk07SM3x1G5PqowsvvFBOXLBggTpOP75uvcIt6E3p0qUN0oJmejCeG2644eyzz+b8KleurCstja1GjRo4U70SUWBRUCAadrKhChUqaGNUOpTliR99zfNLhJ9molTJMli0IaVGQZ9YHGSQH8PesmWLLNmjRw811GmnnZa0bNiwIcPE/ZjI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"
	
	base64_to_img(data.split(",")[1], "../../image/origina388l.png")
