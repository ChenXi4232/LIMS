from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from .models import Book, BookInfo, LibraryBranch, Reader
from .models import BorrowingInfo, ReservationInfo, LateFeeInfo
from .models import ReaderStudent, ReaderFaculty
from .models import Staff, LibraryDirector, Librarian, SecurityGuard, Janitor
from .models import UserInfo
from .serializers import LibraryBranchSerializer
from .serializers import BookInfoSerializer
from .serializers import BookSerializer
from .serializers import ReaderSerializer
from .serializers import ReaderStudentSerializer
from .serializers import ReaderFacultySerializer
from .serializers import BorrowingInfoSerializer
from .serializers import ReservationInfoSerializer
from .serializers import StaffSerializer
from .serializers import LibraryDirectorSerializer
from .serializers import LibrarianSerializer
from .serializers import SecurityGuardSerializer
from .serializers import JanitorSerializer
from .serializers import UpdateReaderSerializer
from .serializers import UpdateStaffSerializer
from .serializers import LateFeeInfoSerializer
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.conf import settings
from django.db import transaction
import os
import datetime
import time
from rest_framework.permissions import BasePermission


class HasLibrarianPermission(BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        # 检查用户是否已认证
        if not request.user.is_authenticated:
            return False
        # 检查用户是否具有特定权限
        if request.user.roles == 'Librarian' or request.user.roles == 'LibraryDirector' or request.user.is_superuser:
            return True
        return False


class HasReaderPermission(BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        # 检查用户是否已认证
        if not request.user.is_authenticated:
            return False
        # 检查用户是否具有特定权限
        if request.user.roles == 'Reader' or request.user.roles == 'Librarian' or request.user.roles == 'LibraryDirector' or request.user.is_superuser:
            return True
        return False


class HasStaffPermission(BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        # 检查用户是否已认证
        if not request.user.is_authenticated:
            return False
        # 检查用户是否具有特定权限
        if request.user.roles == 'Staff' or request.user.roles == 'Librarian' or request.user.roles == 'LibraryDirector' or request.user.is_superuser:
            return True
        return False


class HasLibraryDirectorPermission(BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        # 检查用户是否已认证
        if not request.user.is_authenticated:
            return False
        # 检查用户是否具有特定权限
        if request.user.roles == 'LibraryDirector' or request.user.is_superuser:
            return True
        return False


class HasSuperuserPermission(BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        # 检查用户是否已认证
        if not request.user.is_authenticated:
            return False
        # 检查用户是否具有特定权限
        if request.user.is_superuser:
            return True
        return False


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
# @permission_classes([])
def get_user_info(request):
    if request.method == 'GET':
        user = request.user
        data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "avatar": "",
            # "groups":user_object.groups,
            "roles": user.roles,
            "introduction": user.introduction
        }
        re_data = {"data": data,
                   "code": 20000,
                   "message": "success"
                   }

        return Response(re_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([HasSuperuserPermission])
def create_library_branch(request):
    if request.method == 'POST':
        serializer = LibraryBranchSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([HasLibrarianPermission])
def create_book_info(request):
    if request.method == 'POST':
        print(request.data)
        serializer = BookInfoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    re_data = {
                        "data": serializer.data,
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([HasLibrarianPermission])
def create_book(request):
    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    re_data = {
                        "data": serializer.data,
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([HasLibrarianPermission])
def create_reader(request):
    if request.method == 'POST':
        # print(request.data)
        serializer = ReaderSerializer(data=request.data)
        if serializer.is_valid():
            # try:
            with transaction.atomic():
                serializer.save()
                # 创建用户
                user = UserInfo.objects.create_user(
                    username=serializer.validated_data['reader_card_id'], password="111111", roles='Reader')
                user.save()
                re_data = {
                    "data": serializer.data,
                    "code": 20000,
                    "message": "success"
                }
                return Response(re_data, status=status.HTTP_201_CREATED)
            # except Exception as e:
            #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 修改密码
@api_view(['POST'])
def change_password(request):
    if request.method == 'POST':
        user = request.user
        password = request.data.get('password')
        user.set_password(password)
        user.save()
        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([HasLibrarianPermission])
def create_reader_student(request):
    if request.method == 'POST':
        serializer = ReaderStudentSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.is_valid():
                # 检查是否已经有读者类型注册，若有则返回 400
                reader_card_id = serializer.validated_data['reader_card_id']
                signFaculty = ReaderFaculty.objects.filter(reader_card_id=reader_card_id)
                signStudent = ReaderStudent.objects.filter(reader_card_id=reader_card_id)
                if signFaculty.exists() or signStudent.exists():
                    return Response({"error": "Reader type already exists."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                with transaction.atomic():
                    serializer.save()
                    re_data = {
                        "data": serializer.data,
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([HasLibrarianPermission])
def create_reader_faculty(request):
    if request.method == 'POST':
        serializer = ReaderFacultySerializer(data=request.data)
        if serializer.is_valid():
            # 检查是否已经有读者类型注册，若有则返回 400
            reader_card_id = serializer.validated_data['reader_card_id']
            signFaculty = ReaderFaculty.objects.filter(reader_card_id=reader_card_id)
            signStudent = ReaderStudent.objects.filter(reader_card_id=reader_card_id)
            if signFaculty.exists() or signStudent.exists():
                return Response({"error": "Reader type already exists."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                with transaction.atomic():
                    serializer.save()
                    re_data = {
                        "data": serializer.data,
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([HasReaderPermission])
def create_borrowing_info(request):
    if request.method == 'POST':
        # print(request.data)
        serializer = BorrowingInfoSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            serializer.validated_data['due_date'] = datetime.date.today() + datetime.timedelta(days=60)
            reader_card_id = serializer.validated_data['reader_card_id']
            try:
                # 检查读者证有效期，到期则无法借书
                reader = Reader.objects.get(pk=reader_card_id)
                if reader.expiration_date < datetime.date.today():
                    return Response({"error": "Reader card has expired."}, status=status.HTTP_400_BAD_REQUEST)
                # 检查读者借阅数量，超限无法借书
                if reader.borrowing_count >= reader.borrowing_limit:
                    return Response({"error": "Reader has reached borrowing limit."},
                                    status=status.HTTP_400_BAD_REQUEST)
                book = Book.objects.get(pk=book_id)
                if book.status == 'B' or book.status == 'BR':
                    return Response({"error": "Book is already borrowed by others."},
                                    status=status.HTTP_400_BAD_REQUEST)
                if book.status == 'R':
                    # 查询是否是预约读者且是否超过预约期限
                    reservationinfo = ReservationInfo.objects.filter(book_id=book_id, reader_card_id=reader_card_id,
                                                                     pickup_date=None)
                    if not reservationinfo.exists():
                        return Response({"error": "Book is already reserved by others."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    sign = False
                    for reservation in reservationinfo:
                        if reservation.reservation_date + datetime.timedelta(days=3) >= datetime.date.today():
                            sign = True
                            break
                    if not sign:
                        return Response({
                            "error": "Your reservation have been late_fine. Book is reserved by others and you cannot borrow it."},
                            status=status.HTTP_400_BAD_REQUEST)
                try:
                    with transaction.atomic():
                        serializer.save()
                        re_data = {
                            "data": serializer.data,
                            "code": 20000,
                            "message": "success"
                        }
                        return Response(re_data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # except Book.DoesNotExist:
            #     return Response({"error": "Book does not exist."}, status=status.HTTP_404_NOT_FOUND)
            # 书或读者不存在
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([HasReaderPermission])
def create_reservation_info(request):
    if request.method == 'POST':
        serializer = ReservationInfoSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            reader_card_id = serializer.validated_data['reader_card_id']
            try:
                # 检查读者证有效期，到期则无法借书
                reader = Reader.objects.get(pk=reader_card_id)
                if reader.expiration_date < datetime.date.today():
                    return Response({"error": "Reader card has expired."}, status=status.HTTP_400_BAD_REQUEST)
                if reader.borrowing_count >= reader.borrowing_limit:
                    return Response({"error": "Reader has reached borrowing limit."},
                                    status=status.HTTP_400_BAD_REQUEST)
                book = Book.objects.get(pk=book_id)
                # 检查书籍是否已预约
                if book.status == 'R' or book.status == 'BR':
                    return Response({"error": "Book is already reserved."}, status=status.HTTP_400_BAD_REQUEST)
                # 借书的人不能预约
                borrowinfo = BorrowingInfo.objects.filter(book_id=book_id, reader_card_id=reader_card_id,
                                                          return_date=None)
                if borrowinfo.exists():
                    return Response({"error": "Book is already borrowed by you."}, status=status.HTTP_400_BAD_REQUEST)
                # 预约且三天内未取书的人从预约日算起十天内不得再次预约
                reservationinfo = ReservationInfo.objects.filter(book_id=book_id, reader_card_id=reader_card_id,
                                                                 pickup_date=None)
                if reservationinfo.exists():
                    sign1 = False
                    for reservation in reservationinfo:
                        if reservation.reservation_date + datetime.timedelta(days=3) < datetime.date.today():
                            if reservation.reservation_date + datetime.timedelta(days=10) >= datetime.date.today():
                                sign1 = True
                                break
                    if sign1:
                        return Response({
                            "error": "You have already reserved this book within past ten days but didn't take it, so you cannot reserve it again."},
                            status=status.HTTP_400_BAD_REQUEST)
                reservationinfo = ReservationInfo.objects.filter(reader_card_id=reader_card_id, pickup_date=None)
                sign2 = False
                for reservation in reservationinfo:
                    if reservation.reservation_date + datetime.timedelta(days=3) >= datetime.date.today():
                        sign2 = True
                        break
                if sign2:
                    return Response({
                        "error": "You have already reserved this book within past three days and not take it, so you cannot reserve it again."},
                        status=status.HTTP_400_BAD_REQUEST)
                try:
                    with transaction.atomic():
                        # 创建预约
                        serializer.save()
                        re_data = {
                            "data": serializer.data,
                            "code": 20000,
                            "message": "success"
                        }
                        return Response(re_data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([HasLibraryDirectorPermission])
def create_staff(request):
    if request.method == 'POST':
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    # 同时创建用户
                    user = UserInfo.objects.create_user(
                        username=serializer.validated_data['staff_id'], password="111111", roles='staff')
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([HasLibraryDirectorPermission])
def create_library_director(request):
    if request.method == 'POST':
        serializer = LibraryDirectorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    # 创建用户
                    user = UserInfo.objects.create_user(
                        username=serializer.validated_data['staff_id'], password="111111", roles='LibraryDirector')
                    user.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([HasLibraryDirectorPermission])
def create_librarian(request):
    if request.method == 'POST':
        serializer = LibrarianSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    # 创建用户
                    user = UserInfo.objects.create_user(
                        username=serializer.validated_data['staff_id'], password="111111", roles='Librarian')
                    user.save()
                    re_data = {
                        "data": serializer.data,
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([HasLibraryDirectorPermission])
def create_security_guard(request):
    if request.method == 'POST':
        serializer = SecurityGuardSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([HasLibraryDirectorPermission])
def create_janitor(request):
    if request.method == 'POST':
        serializer = JanitorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 续借
@api_view(['POST'])
def renew_book(request):
    if request.method == 'POST':
        borrowing_id = request.data['borrowing_id']
        try:
            borrowing_info = BorrowingInfo.objects.get(pk=borrowing_id)
            if borrowing_info.is_renewed:
                return Response({"error": "Book has been renewed once."}, status=status.HTTP_400_BAD_REQUEST)
            borrowing_info.is_renewed = True
            borrowing_info.due_date += datetime.timedelta(days=30)
            try:
                with transaction.atomic():
                    borrowing_info.save()
                    re_data = {
                        "data": request.data,
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except BorrowingInfo.DoesNotExist:
            return Response({"error": "Borrowing info does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 取消预约，即删除预约记录
@api_view(['DELETE'])
@permission_classes([HasReaderPermission])
def cancel_reservation(request):
    if request.method == 'DELETE':
        reservation_id = request.data['reservation_id']
        try:
            reservation_info = ReservationInfo.objects.get(pk=reservation_id)
            # 超过预约时间 3 天后无法取消预约
            if reservation_info.reservation_date + datetime.timedelta(days=3) < datetime.date.today():
                return Response({"error": "Reservation has been late_fine."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                with transaction.atomic():
                    reservation_info.delete()
                    re_data = {
                        "data": request.data,
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ReservationInfo.DoesNotExist:
            return Response({"error": "Reservation info does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only DELETE method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 还书
@api_view(['POST'])
def return_book(request):
    if request.method == 'POST':
        borrowing_id = int(request.data['borrowing_id'])
        try:
            borrowing_info = BorrowingInfo.objects.get(pk=borrowing_id)
            if borrowing_info.return_date:
                return Response({"error": "Book has been returned."}, status=status.HTTP_400_BAD_REQUEST)
            borrowing_info.return_date = datetime.date.today()
            try:
                with transaction.atomic():
                    borrowing_info.save()
                    re_data = {
                        "data": request.data,
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except BorrowingInfo.DoesNotExist:
            return Response({"error": "Borrowing info does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 更新 Book 馆藏位置
@api_view(['POST'])
@permission_classes([HasLibrarianPermission])
def update_book_location(request):
    if request.method == 'POST':
        book_id = request.data['book_id']
        branch_location = request.data['branch_location']
        try:
            with transaction.atomic():
                Book.objects.filter(pk=book_id).update(branch_location=branch_location)
                re_data = {
                    "data": request.data,
                    "code": 20000,
                    "message": "success"
                }
                return Response(re_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 删除 Book ，如果未还必须先设置还书
@api_view(['DELETE'])
@permission_classes([HasLibrarianPermission])
def delete_book(request):
    if request.method == 'DELETE':
        try:
            book_id = request.data['book_id']
            book = Book.objects.get(pk=book_id)
            if book.status == 'B' or book.status == 'BR':
                return Response({"error": "Book is not returned yet."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                with transaction.atomic():
                    book.delete()
                    re_data = {
                        "data": [],
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Book.DoesNotExist:
            return Response({"error": "Book does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only DELETE method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 修改 BookInfo 信息
@api_view(['POST'])
@permission_classes([HasLibrarianPermission])
def update_book_info(request):
    if request.method == 'POST':
        call_number = request.data['call_number']
        try:
            book_info = BookInfo.objects.get(pk=call_number)
            if 'title' in request.data:
                book_info.title = request.data['title']
            if 'publisher' in request.data:
                book_info.publisher = request.data['publisher']
            if 'description' in request.data:
                book_info.description = request.data['description']
            if 'isbn' in request.data:
                book_info.isbn = request.data['isbn']
            if 'cover_image_path' in request.data:
                # 删除原路径图片
                if book_info.cover_image_path != request.data['cover_image_path']:
                    if book_info.cover_image_path:
                        os.remove(str(settings.BASE_DIR) + book_info.cover_image_path)
                book_info.cover_image_path = request.data['cover_image_path']
            if 'price' in request.data:
                book_info.price = request.data['price']
            if 'category' in request.data:
                book_info.category = request.data['category']
            if 'publication_date' in request.data:
                book_info.publication_date = request.data['publication_date']
            if 'author' in request.data:
                book_info.author = request.data['author']
            try:
                with transaction.atomic():
                    book_info.save()
                    re_data = {
                        "data": request.data,
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except BookInfo.DoesNotExist:
            return Response({"error": "Book info does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 更新读者信息
@api_view(['POST'])
@permission_classes([HasReaderPermission])
def update_reader(request):
    if request.method == 'POST':
            reader_card_id = request.data['reader_card_id']
            try:
                reader = Reader.objects.get(pk=reader_card_id)
                if request.data['name'] != "":
                    reader.name = request.validated_data['name']
                if request.data['address'] != "":
                    reader.address = request.validated_data['address']
                if request.data['phone_number'] != "":
                    reader.phone_number = request.validated_data['phone_number']
                if request.data['email'] != "":
                    reader.email = request.data['email']
                if request.data['gender'] != "":
                    reader.gender = request.data['gender']
                if request.data['reader_card_photo'] != "":
                    reader.reader_card_photo = request.data['reader_card_photo']
                if request.data['date_of_birth'] != "":
                    reader.date_of_birth = request.data['date_of_birth']
                try:
                    with transaction.atomic():
                        reader.save()
                        re_data = {
                            "data": request.data,
                            "code": 20000,
                            "message": "success"
                        }
                        return Response(re_data, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Reader.DoesNotExist:
                return Response({"error": "Reader does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 删除 bookinfo
@api_view(['DELETE'])
@permission_classes([HasLibrarianPermission])
def delete_book_info(request):
    if request.method == 'DELETE':
        # print(request.data)
        call_number = request.data['call_number']
        # print(call_number.type)
        book_info = BookInfo.objects.get(pk=call_number)
        # print(str(settings.BASE_DIR) + book_info.cover_image_path)
        try:
            call_number = request.data['call_number']
            # print(call_number.type)
            book_info = BookInfo.objects.get(pk=call_number)
            # 如果 bookinfo 的书本总数不为0，那么查找所有 call_number 为 call_number 的 book,
            # 执行 book 的删除操作
            if book_info.total_quantity != 0:
                books = Book.objects.filter(call_number=call_number)
                for book in books:
                    if book.status == 'B' or book.status == 'BR':
                        return Response({"error": "Book is not returned yet."}, status=status.HTTP_400_BAD_REQUEST)
                    try:
                        with transaction.atomic():
                            book.delete()
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            try:
                with transaction.atomic():
                    # 同时删除数据库 cover_image_path 对应的图片
                    if book_info.cover_image_path:
                        os.remove(str(settings.BASE_DIR) + book_info.cover_image_path)
                    book_info.delete()
                    re_data = {
                        "data": [],
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except BookInfo.DoesNotExist:
            return Response({"error": "Book info does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only DELETE method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 删除读者
@api_view(['DELETE'])
@permission_classes([HasLibrarianPermission])
def delete_reader(request):
    if request.method == 'DELETE':
        try:
            reader_card_id = request.data['reader_card_id']
            reader = Reader.objects.get(pk=reader_card_id)
            # 从 StudentReader 和 FacultyReader 中找到对应 reader_card_id 的记录并删除
            sign = False
            if not sign:
                try:
                    reader_student = ReaderStudent.objects.get(pk=reader_card_id)
                    sign = True
                    try:
                        with transaction.atomic():
                            reader_student.delete()
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except ReaderStudent.DoesNotExist:
                    pass
            if not sign:
                try:
                    reader_faculty = ReaderFaculty.objects.get(pk=reader_card_id)
                    sign = True
                    try:
                        with transaction.atomic():
                            reader_faculty.delete()
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except ReaderFaculty.DoesNotExist:
                    pass
            try:
                with transaction.atomic():
                    reader.delete()
                    # 同时注销用户
                    user = UserInfo.objects.get(username=reader_card_id)
                    user.delete()
                    re_data = {
                        "data": request.data,
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Reader.DoesNotExist:
            return Response({"error": "Reader does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only DELETE method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 修改指定 reader_card_id 的学生读者的姓名或者学号
@api_view(['POST'])
@permission_classes([HasReaderPermission])
def update_reader_student(request):
    if request.method == 'POST':
        reader_card_id = request.data['reader_card_id']
        try:
            reader_student = ReaderStudent.objects.get(pk=reader_card_id)
            if request.data['major'] != "":
                reader_student.major = request.data['major']
            if request.data['student_id'] != "":
                reader_student.student_id = request.data['student_id']
            try:
                with transaction.atomic():
                    reader_student.save()
                    re_data = {
                        "data": request.data,
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ReaderStudent.DoesNotExist:
            return Response({"error": "Reader student does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 删除指定 reader_card_id 的学生读者
@api_view(['DELETE'])
@permission_classes([HasLibrarianPermission])
def delete_reader_student(request, reader_card_id):
    if request.method == 'DELETE':
        try:
            reader_student = ReaderStudent.objects.get(pk=reader_card_id)
            try:
                with transaction.atomic():
                    reader_student.delete()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ReaderStudent.DoesNotExist:
            return Response({"error": "Reader student does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only DELETE method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 修改指定 reader_card_id 的教职工读者的部门或者工号
@api_view(['POST'])
@permission_classes([HasReaderPermission])
def update_reader_faculty(request):
    if request.method == 'POST':
        print(request.data)
        reader_card_id = request.data['reader_card_id']
        try:
            reader_faculty = ReaderFaculty.objects.get(pk=reader_card_id)
            if request.data['department'] != "":
                reader_faculty.department = request.data['department']
            if request.data['faculty_id'] != "":
                reader_faculty.faculty_id = request.data['faculty_id']
            try:
                with transaction.atomic():
                    reader_faculty.save()
                    re_data = {
                        "data": request.data,
                        "code": 20000,
                        "message": "success"
                    }
                    return Response(re_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ReaderFaculty.DoesNotExist:
            return Response({"error": "Reader faculty does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 删除指定 reader_card_id 的教职工读者
@api_view(['DELETE'])
@permission_classes([HasLibrarianPermission])
def delete_reader_faculty(request, reader_card_id):
    if request.method == 'DELETE':
        try:
            reader_faculty = ReaderFaculty.objects.get(pk=reader_card_id)
            try:
                with transaction.atomic():
                    reader_faculty.delete()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ReaderFaculty.DoesNotExist:
            return Response({"error": "Reader faculty does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only DELETE method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 修改 LateFeeInfo 的处理状态
@api_view(['POST'])
@permission_classes([HasLibrarianPermission])
def update_late_fee_info(request):
    if request.method == 'POST':
        serializer = LateFeeInfoSerializer(data=request.data)
        if serializer.is_valid():
            late_fee_id = serializer.validated_data['late_fee_id']
            try:
                late_fee_info = LateFeeInfo.objects.get(pk=late_fee_id)
                late_fee_info.status = serializer.validated_data['status']
                try:
                    with transaction.atomic():
                        late_fee_info.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except LateFeeInfo.DoesNotExist:
                return Response({"error": "Late fee info does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 删除图书馆分馆
@api_view(['DELETE'])
@permission_classes([HasSuperuserPermission])
def delete_library_branch(request, branch_id):
    if request.method == 'DELETE':
        try:
            library_branch = LibraryBranch.objects.get(pk=branch_id)
            if library_branch.staff_number != 0:
                return Response({"error": "Library branch still has staff."}, status=status.HTTP_400_BAD_REQUEST)
            if library_branch.book_number != 0:
                return Response({"error": "Library branch still has books."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                with transaction.atomic():
                    library_branch.delete()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except LibraryBranch.DoesNotExist:
            return Response({"error": "Library branch does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only DELETE method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 更新 LibraryBranch 的信息
@api_view(['POST'])
@permission_classes([HasLibraryDirectorPermission])
def update_library_branch(request):
    if request.method == 'POST':
        serializer = LibraryBranchSerializer(data=request.data)
        if serializer.is_valid():
            branch_id = serializer.validated_data['branch_id']
            try:
                library_branch = LibraryBranch.objects.get(pk=branch_id)
                if 'branch_name' in serializer.validated_data:
                    library_branch.branch_name = serializer.validated_data['branch_name']
                if 'address' in serializer.validated_data:
                    library_branch.address = serializer.validated_data['address']
                if 'phone_number' in serializer.validated_data:
                    library_branch.phone_number = serializer.validated_data['phone_number']
                if 'email' in serializer.validated_data:
                    library_branch.email = serializer.validated_data['email']
                if 'opening_hours' in serializer.validated_data:
                    library_branch.opening_hours = serializer.validated_data['opening_hours']
                try:
                    with transaction.atomic():
                        library_branch.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except LibraryBranch.DoesNotExist:
                return Response({"error": "Library branch does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 修改 Staff 的信息
@api_view(['POST'])
@permission_classes([HasStaffPermission])
def update_staff(request):
    if request.method == 'POST':
        serializer = UpdateStaffSerializer(data=request.data)
        if serializer.is_valid():
            staff_id = serializer.validated_data['staff_id']
            try:
                staff = Staff.objects.get(pk=staff_id)
                if 'name' in serializer.validated_data:
                    staff.name = serializer.validated_data['name']
                if 'phone_number' in serializer.validated_data:
                    staff.phone_number = serializer.validated_data['phone_number']
                if 'email' in serializer.validated_data:
                    staff.email = serializer.validated_data['email']
                if 'gender' in serializer.validated_data:
                    staff.gender = serializer.validated_data['gender']
                if 'position' in serializer.validated_data:
                    staff.position = serializer.validated_data['position']
                if 'photo' in serializer.validated_data:
                    staff.photo = serializer.validated_data['photo']
                if 'birth_date' in serializer.validated_data:
                    staff.birth_date = serializer.validated_data['birth_date']
                if 'branch_id' in serializer.validated_data:
                    staff.branch_id = serializer.validated_data['branch_id']
                try:
                    with transaction.atomic():
                        staff.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Staff.DoesNotExist:
                return Response({"error": "Staff does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 修改 LibraryDirector 的信息
@api_view(['POST'])
@permission_classes([HasStaffPermission])
def update_library_director(request):
    if request.method == 'POST':
        serializer = LibraryDirectorSerializer(data=request.data)
        if serializer.is_valid():
            staff_id = serializer.validated_data['staff_id']
            try:
                library_director = LibraryDirector.objects.get(pk=staff_id)
                if 'office_address' in serializer.validated_data:
                    library_director.office_address = serializer.validated_data['office_address']
                try:
                    with transaction.atomic():
                        library_director.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except LibraryDirector.DoesNotExist:
                return Response({"error": "Library director does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 删除 LibraryDirector 的信息
@api_view(['DELETE'])
@permission_classes([HasSuperuserPermission])
def delete_library_director(request, staff_id):
    if request.method == 'DELETE':
        try:
            library_director = LibraryDirector.objects.get(pk=staff_id)
            try:
                with transaction.atomic():
                    library_director.delete()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except LibraryDirector.DoesNotExist:
            return Response({"error": "Library director does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only DELETE method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 修改 Librarian 的信息
@api_view(['POST'])
@permission_classes([HasStaffPermission])
def update_librarian(request):
    if request.method == 'POST':
        serializer = LibrarianSerializer(data=request.data)
        if serializer.is_valid():
            staff_id = serializer.validated_data['staff_id']
            try:
                librarian = Librarian.objects.get(pk=staff_id)
                if "expertise" in serializer.validated_data:
                    librarian.expertise = serializer.validated_data['expertise']
                if "responsible_area" in serializer.validated_data:
                    librarian.responsible_area = serializer.validated_data['responsible_area']
                try:
                    with transaction.atomic():
                        librarian.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Librarian.DoesNotExist:
                return Response({"error": "Librarian does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 删除 Librarian 的信息
@api_view(['DELETE'])
@permission_classes([HasLibraryDirectorPermission])
def delete_librarian(request, staff_id):
    if request.method == 'DELETE':
        try:
            librarian = Librarian.objects.get(pk=staff_id)
            try:
                with transaction.atomic():
                    librarian.delete()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Librarian.DoesNotExist:
            return Response({"error": "Librarian does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only DELETE method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 修改 SecurityGuard 的信息
@api_view(['POST'])
@permission_classes([HasStaffPermission])
def update_security_guard(request):
    if request.method == 'POST':
        serializer = SecurityGuardSerializer(data=request.data)
        if serializer.is_valid():
            staff_id = serializer.validated_data['staff_id']
            try:
                security_guard = SecurityGuard.objects.get(pk=staff_id)
                if "shift" in serializer.validated_data:
                    security_guard.shift = serializer.validated_data['shift']
                if "has_training_certificate" in serializer.validated_data:
                    security_guard.has_training_certificate = serializer.validated_data['phas_training_certificate']
                if "responsible_area" in serializer.validated_data:
                    security_guard.responsible_area = serializer.validated_data['responsible_area']
                try:
                    with transaction.atomic():
                        security_guard.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except SecurityGuard.DoesNotExist:
                return Response({"error": "Security guard does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 删除 SecurityGuard 的信息
@api_view(['DELETE'])
@permission_classes([HasLibraryDirectorPermission])
def delete_security_guard(request, staff_id):
    if request.method == 'DELETE':
        try:
            security_guard = SecurityGuard.objects.get(pk=staff_id)
            try:
                with transaction.atomic():
                    security_guard.delete()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except SecurityGuard.DoesNotExist:
            return Response({"error": "Security guard does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only DELETE method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 修改 Janitor 的信息
@api_view(['POST'])
@permission_classes([HasStaffPermission])
def update_janitor(request):
    if request.method == 'POST':
        serializer = JanitorSerializer(data=request.data)
        if serializer.is_valid():
            staff_id = serializer.validated_data['staff_id']
            try:
                janitor = Janitor.objects.get(pk=staff_id)
                if "shift" in serializer.validated_data:
                    janitor.shift = serializer.validated_data['shift']
                if "responsible_area" in serializer.validated_data:
                    janitor.responsible_area = serializer.validated_data['responsible_area']
                try:
                    with transaction.atomic():
                        janitor.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Janitor.DoesNotExist:
                return Response({"error": "Janitor does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 删除 Janitor 的信息
@api_view(['DELETE'])
@permission_classes([HasLibraryDirectorPermission])
def delete_janitor(request, staff_id):
    if request.method == 'DELETE':
        try:
            janitor = Janitor.objects.get(pk=staff_id)
            try:
                with transaction.atomic():
                    janitor.delete()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Janitor.DoesNotExist:
            return Response({"error": "Janitor does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only DELETE method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 删除 Staff
@api_view(['DELETE'])
@permission_classes([HasLibraryDirectorPermission])
def delete_staff(request, staff_id):
    if request.method == 'DELETE':
        try:
            staff = Staff.objects.get(pk=staff_id)
            # 从 LibraryDirector, Librarian, SecurityGuard, Janitor 中找到对应 staff_id 的记录并删除
            sign = False
            if not sign:
                try:
                    library_director = LibraryDirector.objects.get(pk=staff_id)
                    sign = True
                    try:
                        with transaction.atomic():
                            library_director.delete()
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except LibraryDirector.DoesNotExist:
                    pass
            if not sign:
                try:
                    librarian = Librarian.objects.get(pk=staff_id)
                    sign = True
                    try:
                        with transaction.atomic():
                            librarian.delete()
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Librarian.DoesNotExist:
                    pass
            if not sign:
                try:
                    security_guard = SecurityGuard.objects.get(pk=staff_id)
                    sign = True
                    try:
                        with transaction.atomic():
                            security_guard.delete()
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except SecurityGuard.DoesNotExist:
                    pass
            if not sign:
                try:
                    janitor = Janitor.objects.get(pk=staff_id)
                    sign = True
                    try:
                        with transaction.atomic():
                            janitor.delete()
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Janitor.DoesNotExist:
                    pass
            try:
                with transaction.atomic():
                    staff.delete()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Staff.DoesNotExist:
            return Response({"error": "Staff does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only DELETE method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 按照书名正则匹配检索书目并返回 book_info 的信息
@api_view(['POST'])
@permission_classes([HasReaderPermission])
def search_book_info(request):
    temp_query = {'title__regex': request.data['title'], 'publisher__regex': request.data['publisher'],
                  'call_number__regex': request.data['call_number']}
    list_query = {}
    for key in temp_query:
        if temp_query[key] != '':
            list_query[key] = temp_query[key]
    book_info = BookInfo.objects.filter(**list_query)
    serializer = BookInfoSerializer(book_info, many=True)
    # 统计总返回数据数目
    total = len(serializer.data)
    # if not serializer.data:
    #     return Response({"error": "No book info exists."}, status=status.HTTP_404_NOT_FOUND)
    re_data = {
        "data": {
            "total": total,
            "items": serializer.data,
        },
        "code": 20000,
        "message": "success"
    }
    return Response(re_data, status=status.HTTP_200_OK)


# 返回数据库中所有的书目信息
@api_view(['GET'])
@permission_classes([])
def get_all_book_info(request):
    book_info = BookInfo.objects.all()
    serializer = BookInfoSerializer(book_info, many=True)
    total = len(serializer.data)
    re_data = {
        "data": {
            "total": total,
            "items": serializer.data,
        },
        "code": 20000,
        "message": "success"
    }
    return Response(re_data, status=status.HTTP_200_OK)


# 获取同一索书号下所有书的借阅状态和馆藏位置
@api_view(['POST'])
@permission_classes([])
def get_books_by_call_number(request):
    if request.method == 'POST':
        # print(request.data)
        call_number = request.data['call_number']
        # print(call_number)
        books = Book.objects.filter(call_number=call_number)
        serializer = BookSerializer(books, many=True)
        # 检查每个 branch_location 并替换为对应分馆名称
        for book in serializer.data:
            branch_location_id = book['branch_location']
            branch = LibraryBranch.objects.get(pk=branch_location_id)
            book['branch_location'] = branch.branch_name
            book_id = book['book_id']
            # 检查每本书的借阅状态
            book_item = Book.objects.get(pk=book_id)
            book['status'] = book_item.get_status_display()
        total = len(serializer.data)
        # print(serializer.data)
        re_data = {
            "data": {
                "total": total,
                "items": serializer.data,
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 返回数据库中对应 read_card_id 的读者信息
@api_view(['POST'])
@permission_classes([HasReaderPermission])
def get_reader(request):
    try:
        reader_card_id = request.data["name"]
        reader = Reader.objects.get(pk=reader_card_id)
        serializer = ReaderSerializer(reader)
        # 确认读者类型
        type = None
        data = None
        try:
            data = ReaderStudent.objects.get(pk=reader_card_id)
            type = "student"
        except ReaderStudent.DoesNotExist:
            pass
        if not type:
            try:
                data = ReaderFaculty.objects.get(pk=reader_card_id)
                type = "faculty"
            except ReaderFaculty.DoesNotExist:
                pass
        re_data = {
            "data": {
                "type": type,
                "reader": serializer.data,
                "extra": data
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    except Reader.DoesNotExist:
        return Response({"error": "Reader does not exist."}, status=status.HTTP_404_NOT_FOUND)


# 上传书本图片
@api_view(['POST'])
@permission_classes([HasLibrarianPermission])
def upload_book_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        # 按照当前时间重命名
        save_path = os.path.join(settings.MEDIA_ROOT, 'figs', 'book', str(int(time.time())) + file.name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        image_url = os.path.join(settings.MEDIA_URL, 'figs', 'book', str(int(time.time())) + file.name)
        re_data = {
            "data": {
                "image_url": image_url
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)


# 上传员工照片
@api_view(['POST'])
@permission_classes([HasStaffPermission])
def upload_staff_photo(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        # 按照当前时间重命名
        save_path = os.path.join(settings.MEDIA_ROOT, 'figs', 'staff', str(int(time.time())) + file.name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        image_url = os.path.join(settings.MEDIA_URL, 'figs', 'staff', str(int(time.time())) + file.name)
        re_data = {
            "data": {
                "image_url": image_url
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)


# 上传读者证件照片
@api_view(['POST'])
@permission_classes([HasReaderPermission])
def upload_reader_card_photo(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        # 按照当前时间重命名
        save_path = os.path.join(settings.MEDIA_ROOT, 'figs', 'reader', str(int(time.time())) + file.name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        image_url = os.path.join(settings.MEDIA_URL, 'figs', 'reader', str(int(time.time())) + file.name)
        re_data = {
            "data": {
                "image_url": image_url
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)


# 获取所有借阅信息
@api_view(['GET'])
@permission_classes([HasLibrarianPermission])
def get_all_borrowing_info(request):
    if request.method == 'GET':
        borrowing_info = BorrowingInfo.objects.all()
        serializer = BorrowingInfoSerializer(borrowing_info, many=True)
        total = len(serializer.data)
        re_data = {
            "data": {
                "total": total,
                "items": serializer.data,
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    return Response({"error": "Only GET method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 查找指定借书记录，book_id、reader_card_id、borrowing_date、return_date，其中多个
@api_view(['POST'])
@permission_classes([HasReaderPermission])
def search_borrowing_info(request):
    if request.method == 'POST':
        temp_query = {'book_id': request.data['book_id'], 'reader_card_id': request.data['reader_card_id'],
                      'borrowing_date': request.data['borrowing_date'], 'return_date': request.data['return_date']}
        list_query = {}
        for key in temp_query:
            if temp_query[key] != '':
                list_query[key] = temp_query[key]
        borrowing_info = BorrowingInfo.objects.filter(**list_query)
        serializer = BorrowingInfoSerializer(borrowing_info, many=True)
        total = len(serializer.data)
        re_data = {
            "data": {
                "total": total,
                "items": serializer.data,
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 获取所有预约信息
@api_view(['GET'])
@permission_classes([HasLibrarianPermission])
def get_all_reservation_info(request):
    if request.method == 'GET':
        reservation_info = ReservationInfo.objects.all()
        serializer = ReservationInfoSerializer(reservation_info, many=True)
        total = len(serializer.data)
        re_data = {
            "data": {
                "total": total,
                "items": serializer.data,
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    return Response({"error": "Only GET method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 查找指定预约记录，book_id、reader_card_id、reservation_date、pickup_date，其中多个
@api_view(['POST'])
@permission_classes([HasReaderPermission])
def search_reservation_info(request):
    if request.method == 'POST':
        temp_query = {'book_id': request.data['book_id'], 'reader_card_id': request.data['reader_card_id'],
                      'reservation_date': request.data['reservation_date'], 'pickup_date': request.data['pickup_date']}
        list_query = {}
        for key in temp_query:
            if temp_query[key] != '':
                list_query[key] = temp_query[key]
        reservation_info = ReservationInfo.objects.filter(**list_query)
        serializer = ReservationInfoSerializer(reservation_info, many=True)
        total = len(serializer.data)
        re_data = {
            "data": {
                "total": total,
                "items": serializer.data,
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 查询所有逾期信息
@api_view(['GET'])
@permission_classes([HasLibrarianPermission])
def get_all_late_fee_info(request):
    if request.method == 'GET':
        late_fee_info = LateFeeInfo.objects.all()
        serializer = LateFeeInfoSerializer(late_fee_info, many=True)
        for late_fee in serializer.data:
            late_fee_id = late_fee['late_fee_id']
            late_fee_item = LateFeeInfo.objects.get(pk=late_fee_id)
            late_fee['status'] = late_fee_item.get_status_display()
        total = len(serializer.data)
        re_data = {
            "data": {
                "total": total,
                "items": serializer.data,
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    return Response({"error": "Only GET method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 查询指定逾期信息，late_fee_id、reader_card_id、book_id、status，其中多个，status 返回表示处理状态
@api_view(['POST'])
@permission_classes([HasReaderPermission])
def search_late_fee_info(request):
    if request.method == 'POST':
        print(request.data)
        temp_query = {'reader_card_id': request.data['reader_card_id'], 'book_id': request.data['book_id'],
                      'status': request.data['status']}
        list_query = {}
        for key in temp_query:
            if temp_query[key] != '':
                list_query[key] = temp_query[key]
        late_fee_info = LateFeeInfo.objects.filter(**list_query)
        serializer = LateFeeInfoSerializer(late_fee_info, many=True)
        for late_fee in serializer.data:
            late_fee_id = late_fee['late_fee_id']
            late_fee_item = LateFeeInfo.objects.get(pk=late_fee_id)
            late_fee['status'] = late_fee_item.get_status_display()
        total = len(serializer.data)
        re_data = {
            "data": {
                "total": total,
                "items": serializer.data,
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 更改逾期信息状态
@api_view(['POST'])
@permission_classes([HasLibrarianPermission])
def update_late_fee_info_status(request):
    if request.method == 'POST':
        # print(request.data)
        late_fee_id = request.data['late_fee_id']
        try:
            late_fee_info = LateFeeInfo.objects.get(pk=late_fee_id)
            if late_fee_info.status == 'Paid':
                return Response({"error": "Late fee has been paid."}, status=status.HTTP_400_BAD_REQUEST)
            late_fee_info.status = request.data['status']
            # print(late_fee_info.status)
            # try:
            with transaction.atomic():
                late_fee_info.save()
                re_data = {
                    "data": request.data,
                    "code": 20000,
                    "message": "success"
                }
                return Response(re_data, status=status.HTTP_200_OK)
            # except Exception as e:
            #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except LateFeeInfo.DoesNotExist:
            return Response({"error": "Late fee info does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 查找指定读者，利用 reader_card_id、name、phone_number、gender 等信息
@api_view(['POST'])
@permission_classes([HasReaderPermission])
def search_reader(request):
    if request.method == 'POST':
        temp_query = {'reader_card_id': request.data['reader_card_id'], 'name': request.data['name'],
                      'phone_number': request.data['phone_number'], 'gender': request.data['gender']}
        list_query = {}
        for key in temp_query:
            if temp_query[key] != '':
                list_query[key] = temp_query[key]
        reader_info = Reader.objects.filter(**list_query)
        serializer = ReaderSerializer(reader_info, many=True)
        for reader in serializer.data:
            reader_card_id = reader['reader_card_id']
            # type = None
            # data = None
            # try:
            #     data = ReaderStudent.objects.get(pk=reader_card_id)
            #     type = "student"
            # except ReaderStudent.DoesNotExist:
            #     pass
            # if not type:
            #     try:
            #         data = ReaderFaculty.objects.get(pk=reader_card_id)
            #         type = "faculty"
            #     except ReaderFaculty.DoesNotExist:
            #         pass
            # reader_item['type'] = type
            # reader_item['extra'] = data
            reader_item = Reader.objects.get(pk=reader_card_id)
            reader['gender'] = reader_item.get_gender_display()
        total = len(serializer.data)
        # print(serializer.data)
        re_data = {
            "data": {
                "total": total,
                "items": serializer.data,
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 返回所有读者信息
@api_view(['GET'])
@permission_classes([HasLibrarianPermission])
def get_all_reader(request):
    if request.method == 'GET':
        reader_info = Reader.objects.all()
        serializer = ReaderSerializer(reader_info, many=True)
        for reader in serializer.data:
            reader_card_id = reader['reader_card_id']
            # type = None
            # data = None
            # try:
            #     data = ReaderStudent.objects.get(pk=reader_card_id)
            #     type = "student"
            # except ReaderStudent.DoesNotExist:
            #     pass
            # if not type:
            #     try:
            #         data = ReaderFaculty.objects.get(pk=reader_card_id)
            #         type = "faculty"
            #     except ReaderFaculty.DoesNotExist:
            #         pass
            reader_item = Reader.objects.get(pk=reader_card_id)
            reader['gender'] = reader_item.get_gender_display()
        total = len(serializer.data)
        re_data = {
            "data": {
                "total": total,
                "items": serializer.data,
            },
            "code": 20000,
            "message": "success"
        }
        return Response(re_data, status=status.HTTP_200_OK)
    return Response({"error": "Only GET method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# 查找指定 reader_card_id 的读者类型信息
@api_view(['POST'])
@permission_classes([HasReaderPermission])
def search_reader_type(request):
    if request.method == 'POST':
        reader_card_id = request.data['reader_card_id']
        # print(reader_card_id)
        try:
            reader_student = ReaderStudent.objects.get(pk=reader_card_id)
            serializer = ReaderStudentSerializer(reader_student)
            # print(serializer.data)
            re_data = {
                "data": {
                    "type": "student",
                    "info": serializer.data,
                },
                "code": 20000,
                "message": "success"
            }
            return Response(re_data, status=status.HTTP_200_OK)
        except ReaderStudent.DoesNotExist:
            try:
                reader_faculty = ReaderFaculty.objects.get(pk=reader_card_id)
                serializer = ReaderFacultySerializer(reader_faculty)
                # print(serializer.data)
                re_data = {
                    "data": {
                        "type": "faculty",
                        "info": serializer.data,
                    },
                    "code": 20000,
                    "message": "success"
                }
                return Response(re_data, status=status.HTTP_200_OK)
            except ReaderFaculty.DoesNotExist:
                return Response({"error": "Reader does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
