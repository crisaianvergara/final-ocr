from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Scan
from .serializers import ScanSerializer
from PIL import Image
from doctr.models import ocr_predictor
import re
import nltk
from .utils import extract_and_format_date, preprocess, classify_description
from PIL import Image
from io import BytesIO
import numpy as np


class ScanListAPIView(APIView):
    def get(self, request):
        scans = Scan.objects.filter(user=request.user.id)
        serializer = ScanSerializer(scans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        image_data = request.data.get("image")
        image_bytes = BytesIO(image_data.read())
        receipt = Image.open(image_bytes)

        # OCR MODEL
        model = ocr_predictor(
            det_arch="db_resnet50", reco_arch="crnn_mobilenet_v3_small", pretrained=True
        )

        # RUN OCR
        image = [np.array(receipt)]

        result = model(image)

        # OCR RESULT
        blocks = result.export()["pages"][0]["blocks"]
        lines = [line["lines"] for line in blocks]
        values = [word["words"] for line in lines for word in line]

        result = []
        for lst in values:
            text = " ".join([item["value"] for item in lst])
            result.append(text)

        # DATE PATTERNS
        date_patterns = [
            r"\d{1,2}/\d{1,2}/\d{2}",
            r"\s+(\d{1,2}/\d{1,2}/\d{4})",
            r"Date:\s(\d{4}-\d{2}-\d{2})",
            r"\d{2}-\d{2}-\d{2}",
            r"\d{2}/\d{2}/\d{2}",
            r"\d{2}/\d{2}/\d{4}",
            r"\b(\d{1,2} [A-Za-z]{3} \d{2})\b",
            r"\b([A-Z][a-z]{2} \d{1,2},\d{4})\b",
        ]

        # VENDOR
        new_result = [item for item in result if len(item) >= 2]
        vendor = new_result[0].translate(str.maketrans("", "", ".?"))

        # TAX
        format_amount_and_tax = r"\d+\.\d+"

        tax = None

        for i in range(len(result)):
            if "Sales Tax 6.25%" in result[i]:
                tax = re.search(format_amount_and_tax, result[i + 10]).group()
                break
            elif "Sales Tax" in result[i]:
                tax = re.search(format_amount_and_tax, result[i + 2]).group()
                break
            elif "VAT Amount(12%)" in result[i]:
                tax = re.search(format_amount_and_tax, result[i - 6]).group()
                break
            elif "SALES TAX AMOUNT" in result[i]:
                s = result[i - 3]
                tax = re.search(
                    format_amount_and_tax,
                    "${:,.2f}".format(float(s[1:].replace(",", "."))),
                ).group()
                break
            elif "Tax(RM)" in result[i]:
                tax = re.search(format_amount_and_tax, f"0{result[i + 2]}").group()
                break
            elif "TAX 1" in result[i]:
                tax = re.search(format_amount_and_tax, result[i - 37]).group()
                break
            elif "TAX" in result[i]:
                tax = re.search(format_amount_and_tax, result[i - 1]).group()
                break

        # AMOUNT AND CURRENCY
        amount = None
        currency = None

        currency_symbols = {
            "$": "USD",
            "£": "GBP",
            "€": "EUR",
            "¥": "JPY",
            "₩": "KRW",
            "₱": "PHP",
            "P": "PHP",
            "₹": "INR",
        }

        price_regex = r"([\$£€¥₩₱₹])(\d+(?:\.\d{1,2})?)"

        try:
            prices = []
            for item in result:
                match = re.search(price_regex, item)
                if match:
                    symbol = match.group(1)
                    price = float(match.group(2))
                    prices.append(price)
                    if symbol in currency_symbols:
                        currency = currency_symbols[symbol]
            amount = max(prices)

        except ValueError:
            for i in range(len(result)):
                if "Amount" in result[i] and "Due" in result[i + 4]:
                    amount = re.search(format_amount_and_tax, result[i + 5]).group()
                    currency = "PHP"
                    break
                elif "Total:" in result[i]:
                    amount = re.search(format_amount_and_tax, result[i + 4]).group()
                    break
                elif "Total Sales Inclusive GST) RM" in result[i]:
                    amount = re.search(format_amount_and_tax, result[i + 1]).group()
                    break
                elif "SUBTOTAL" in result[i] and "TOTAL" in result[i + 4]:
                    amount = re.search(format_amount_and_tax, result[i - 33]).group()
                    break

        # DESCRIPTION
        # DOWNLOAD REQUIRED NLTK DATA
        nltk.download("punkt", quiet=True)
        nltk.download("wordnet", quiet=True)
        nltk.download("stopwords", quiet=True)

        formatted_date = extract_and_format_date(result, date_patterns)

        for receipt_text in result:
            filtered_words = preprocess(receipt_text)
            description = classify_description(filtered_words)

        data = {
            "date": formatted_date,
            "vendor": vendor,
            "amount": amount,
            "tax": tax,
            "currency": currency,
            "description": description,
            "user": request.user.id,
        }

        serializer = ScanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScanDetailApiView(APIView):
    def get_object(self, scan_id, user_id):
        try:
            return Scan.objects.get(id=scan_id, user_id=user_id)
        except Scan.DoesNotExist:
            return None

    def get(self, request, scan_id):
        scan_instance = self.get_object(scan_id, request.user.id)
        if not scan_instance:
            return Response(
                {"res": "Object with scan id does not exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ScanSerializer(scan_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, scan_id):
        scan_instance = self.get_object(scan_id, request.user.id)
        if not scan_instance:
            return Response(
                {"res": "Object with scan id does not exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "date": request.data.get("date"),
            "vendor": request.data.get("vendor"),
            "amount": request.data.get("amount"),
            "tax": request.data.get("tax"),
            "currency": request.data.get("currency"),
            "description": request.data.get("description"),
            "user": request.user.id,
        }

        serializer = ScanSerializer(instance=scan_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, scan_id):
        scan_instance = self.get_object(scan_id, request.user.id)
        if not scan_instance:
            return Response(
                {"res": "Object with scan id does not exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        scan_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
