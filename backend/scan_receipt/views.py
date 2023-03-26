from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Scan
from .serializers import ScanSerializer
from rest_framework.permissions import AllowAny


class ScanListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        scans = Scan.objects.filter(user=request.user.id)
        serializer = ScanSerializer(scans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "date": request.data.get("date"),
            "vendor": request.data.get("vendor"),
            "amount": request.data.get("amount"),
            "tax": request.data.get("tax"),
            "currency": request.data.get("currency"),
            "description": request.data.get("description"),
            "user": request.user.id,
        }

        serializer = ScanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScanDetailApiView(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, scan_id, user_id):
        try:
            return Scan.objects.get(id=scan_id, user_id=user_id)
        except Scan.DoesNotExist:
            return None

    def get(self, request, scan_id, *args, **kwargs):
        scan_instance = self.get_object(scan_id, request.user.id)
        if not scan_instance:
            return Response(
                {"res": "Object with scan id does not exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ScanSerializer(scan_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, scan_id, *args, **kwargs):
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

    def delete(self, request, scan_id, *args, **kwargs):
        scan_instance = self.get_object(scan_id, request.user.id)
        if not scan_instance:
            return Response(
                {"res": "Object with scan id does not exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        scan_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
