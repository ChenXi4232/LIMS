# serializers.py
import os
import datetime

from django.conf import settings
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from .models import LibraryBranch, BookInfo, Book, Reader
from .models import ReaderStudent, ReaderFaculty
from .models import BorrowingInfo, ReservationInfo, LateFeeInfo
from .models import Staff
from .models import LibraryDirector, Librarian, SecurityGuard, Janitor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['roles'] = user.roles
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        re_data = {'data': data, 'code': 20000, 'message': 'success'}

        return re_data


class LibraryBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBranch
        fields = ['branch_id', 'branch_name', 'address', 'phone_number',
                  'email', 'opening_hours', 'book_number', 'staff_number']
        read_only_fields = ['book_number', 'staff_number']


class BookInfoSerializer(serializers.ModelSerializer):
    # cover_image = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = BookInfo
        fields = ['title', 'publisher', 'description', 'isbn', 'cover_image_path', 'price', 'category',
                  'publication_date', 'author', 'call_number', 'total_quantity', 'borrowable_quantity',
                  'borrowing_count']
        read_only_fields = ['total_quantity', 'borrowable_quantity', 'borrowing_count']

    def create(self, validated_data):
        # 将输入的字符形式的日期转换为datetime格式
        sign1 = None
        publication_date = None
        if 'publication_date' in validated_data:
            sign1 = isinstance(validated_data['publication_date'], str)
            if sign1:
                publication_date = datetime.datetime.strptime(validated_data.pop('publication_date'), '%Y-%m-%d')
        # 将输入的价格字符形式转换为浮点数
        sign2 = None
        price = None
        if 'price' in validated_data:
            sign2 = isinstance(validated_data['price'], str)
            if sign2:
                price = float(validated_data.pop('price'))
        book_info = BookInfo.objects.create(**validated_data)
        if sign1:
            book_info.publication_date = publication_date
        if sign2:
            book_info.price = price
        return book_info

    # def create(self, validated_data):
    #     cover_image = validated_data.pop('cover_image')
    #     book_info = BookInfo.objects.create(**validated_data)
    #     if cover_image:
    #         # 将图片保存到指定目录
    #         book_call_number = book_info.call_number
    #         os.makedirs(os.path.join(settings.MEDIA_ROOT, 'figs/book'), exist_ok=True)
    #         image_base, image_ext = os.path.splitext(cover_image.name)
    #         image_path = os.path.join(settings.MEDIA_ROOT, 'figs/book', book_call_number + image_ext)
    #         with open(image_path, 'wb+') as destination:
    #             for chunk in cover_image.chunks():
    #                 destination.write(chunk)
    #         book_info.cover_image_path = os.path.join(settings.MEDIA_URL, 'figs/book', book_call_number + image_ext)
    #     else:
    #         return Response({"error": "Cover image is required."}, status=status.HTTP_400_BAD_REQUEST)
    #     return book_info


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'call_number', 'status', 'branch_location', 'created_at']
        read_only_fields = ['created_at']


class ReaderSerializer(serializers.ModelSerializer):
    # reader_card_photo = serializers.ImageField(required=True, write_only=True)

    class Meta:
        model = Reader
        fields = ['name', 'address', 'phone_number', 'email', 'gender', 'reader_card_photo',
                  'reader_card_id', 'date_of_birth', 'expiration_date', 'borrowing_limit',
                  'registration_date', 'borrowing_count', 'outstanding_amount']
        read_only_fields = ['registration_date', 'borrowing_limit', 'outstanding_amount', 'borrowing_count']

    def create(self, validated_data):
        # print(validated_data)
        # 将输入的字符形式的日期转换为datetime格式
        sign1 = None
        expiration_date = None
        if 'expiration_date' in validated_data:
            sign1 = isinstance(validated_data['expiration_date'], str)
            if sign1:
                expiration_date = datetime.datetime.strptime(validated_data.pop('expiration_date'), '%Y-%m-%d')
        # 将输入的价格字符形式转换为浮点数
        sign2 = None
        date_of_birth = None
        if 'date_of_birth' in validated_data:
            sign2 = isinstance(validated_data['date_of_birth'], str)
            if sign2:
                date_of_birth = datetime.datetime.strptime(validated_data.pop('date_of_birth'), '%Y-%m-%d')
        # print(validated_data)
        reader = Reader.objects.create(**validated_data)
        if sign1:
            reader.expiration_date = expiration_date
        if sign2:
            reader.date_of_birth = date_of_birth
        return reader

    # def create(self, validated_data):
    #     reader_card_photo = validated_data.pop('reader_card_photo')
    #     reader = Reader.objects.create(**validated_data)
    #     if reader_card_photo:
    #         reader_card_id = reader.reader_card_id
    #         os.makedirs(os.path.join(settings.MEDIA_ROOT, 'figs/reader'), exist_ok=True)
    #         photo_base, photo_ext = os.path.splitext(reader_card_photo.name)
    #         image_path = os.path.join(settings.MEDIA_ROOT, 'figs/reader', reader_card_id + photo_ext)
    #         with open(image_path, 'wb+') as destination:
    #             for chunk in reader_card_photo.chunks():
    #                 destination.write(chunk)
    #         reader.reader_card_photo = os.path.join(settings.MEDIA_URL, 'figs/reader', reader_card_id + photo_ext)
    #     else:
    #         return Response({"error": "Reader card photo is required."}, status=status.HTTP_400_BAD_REQUEST)
    #     reader.expiration_date = reader.registration_date + datetime.timedelta(days=365 * 3)
    #     return reader


class ReaderStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReaderStudent
        fields = "__all__"


class ReaderFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReaderFaculty
        fields = "__all__"


class BorrowingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowingInfo
        fields = ["book_id", "reader_card_id", "due_date", "borrowing_id",
                  "borrowing_date", "return_date", "is_renewed"]
        read_only_fields = ["borrowing_id", "borrowing_date", "return_date", "is_renewed", "due_date"]


class ReservationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationInfo
        fields = ["book_id", "reader_card_id", "reservation_id", "pickup_date", "reservation_date"]
        read_only_fields = ["reservation_id", "pickup_date", "reservation_date"]


class LateFeeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LateFeeInfo
        fields = ["late_fee_id", "status", "reader_card_id", "book_id", "fine_amount", "late_days"]
        read_only_fields = ["reader_card_id", "book_id", "fine_amount", "late_days"]


class StaffSerializer(serializers.ModelSerializer):
    # photo = serializers.ImageField(required=True, write_only=True)

    class Meta:
        model = Staff
        fields = ["name", "phone_number", "email", "gender", "position", "photo_path", "staff_id",
                  "birth_date", "branch_id", "hire_date"]
        read_only_fields = ["hire_date"]

    # def create(self, validated_data):
    #     photo = validated_data.pop('photo')
    #     staff = Staff.objects.create(**validated_data)
    #     if photo:
    #         staff_id = staff.staff_id
    #         photo_base, photo_ext = os.path.splitext(photo.name)
    #         os.makedirs(os.path.join(settings.MEDIA_ROOT, 'figs/staff'), exist_ok=True)
    #         image_path = os.path.join(settings.MEDIA_ROOT, 'figs/staff', staff_id + photo_ext)
    #         with open(image_path, 'wb+') as destination:
    #             for chunk in photo.chunks():
    #                 destination.write(chunk)
    #         staff.photo_path = os.path.join(settings.MEDIA_URL, 'figs/staff', staff_id + photo_ext)
    #     else:
    #         return Response({"error": "Staff photo is required."}, status=status.HTTP_400_BAD_REQUEST)
    #     return staff


class LibraryDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryDirector
        fields = "__all__"


class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = "__all__"


class SecurityGuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityGuard
        fields = "__all__"


class JanitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Janitor
        fields = "__all__"


class UpdateReaderSerializer(serializers.ModelSerializer):
    # reader_card_photo = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = Reader
        fields = ['name', 'address', 'phone_number', 'email', 'gender', 'reader_card_photo',
                  'reader_card_id', 'date_of_birth', 'expiration_data', 'borrowing_limit',
                  'outstanding_amount', 'registration_date', 'borrowing_count']
        read_only_fields = ['registration_date', 'borrowing_count']

    # def create(self, validated_data):
    #     reader_card_photo = None
    #     if 'reader_card_photo' in validated_data:
    #         reader_card_photo = validated_data.pop('reader_card_photo')
    #     reader = Reader.objects.create(**validated_data)
    #     if reader_card_photo:
    #         reader_card_id = reader.reader_card_id
    #         photo_base, photo_ext = os.path.splitext(reader_card_photo.name)
    #         os.makedirs(os.path.join(settings.MEDIA_ROOT, 'figs/reader'), exist_ok=True)
    #         image_path = os.path.join(settings.MEDIA_ROOT, 'figs/reader', reader_card_id + photo_ext)
    #         with open(image_path, 'wb+') as destination:
    #             for chunk in reader_card_photo.chunks():
    #                 destination.write(chunk)
    #         reader.reader_card_photo = os.path.join(settings.MEDIA_URL, 'figs/reader', reader_card_id + photo_ext)
    #     else:
    #         return Response({"error": "Reader card photo is required."}, status=status.HTTP_400_BAD_REQUEST)
    #     return reader


class UpdateStaffSerializer(serializers.ModelSerializer):
    # photo = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = Staff
        fields = ["name", "phone_number", "email", "gender", "position", "photo_path", "staff_id",
                  "birth_date", "branch_id", "hire_date"]
        read_only_fields = ["hire_date"]

    # def create(self, validated_data):
    #     photo = None
    #     if 'photo' in validated_data:
    #         photo = validated_data.pop('reader_card_photo')
    #     staff = Staff.objects.create(**validated_data)
    #     if photo:
    #         staff_id = staff.staff_id
    #         photo_base, photo_ext = os.path.splitext(photo.name)
    #         os.makedirs(os.path.join(settings.MEDIA_ROOT, 'figs/staff'), exist_ok=True)
    #         image_path = os.path.join(settings.MEDIA_ROOT, 'figs/staff', staff_id + photo_ext)
    #         with open(image_path, 'wb+') as destination:
    #             for chunk in photo.chunks():
    #                 destination.write(chunk)
    #         staff.photo = os.path.join(settings.MEDIA_URL, 'figs/staff', staff_id + photo_ext)
    #     else:
    #         return Response({"error": "Staff photo is required."}, status=status.HTTP_400_BAD_REQUEST)
    #     return staff
