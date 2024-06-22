from django.urls import path
from . import views

urlpatterns = [
    path('library-branch/', views.create_library_branch, name='create_library_branch'),
    path('book-info/', views.create_book_info, name='create_book_info'),
    path('book/', views.create_book, name='create_book'),
    path('reader/', views.create_reader, name='create_reader'),
    path('reader-student/', views.create_reader_student, name='create_reader_student'),
    path('reader-faculty/', views.create_reader_faculty, name='create_reader_faculty'),
    path('borrowing-info/', views.create_borrowing_info, name='create_borrowing_info'),
    path('reservation-info/', views.create_reservation_info, name='create_reservation_info'),
    path('staff/', views.create_staff, name='create_staff'),
    path('library-director/', views.create_library_director, name='create_library_director'),
    path('librarian/', views.create_librarian, name='create_librarian'),
    path('security-guard/', views.create_security_guard, name='create_security_guard'),
    path('janitor/', views.create_janitor, name='create_janitor'),
    path('get-user-info/', views.get_user_info, name='get_user_info'),
    path('search-book/', views.search_book_info, name='search_book'),
    path('reset-password/', views.change_password, name='reset_password'),
    path('get-all-books/', views.get_all_book_info, name='get_all_books'),
    path('get-books-by-call-number/', views.get_books_by_call_number, name='get_books_by_call_number'),
    path('get-reader-data/', views.get_reader, name='get_reader_data'),
    path('delete-staff/', views.delete_staff, name='delete_staff'),
    path('delete-reader/', views.delete_reader, name='delete_reader'),
    path('delete-book/', views.delete_book, name='delete_book'),
    path('delete-janitor/', views.delete_janitor, name='delete_janitor'),
    path('update-janitor/', views.update_janitor, name='update_janitor'),
    path('update-staff/', views.update_staff, name='update_staff'),
    path('update-reader/', views.update_reader, name='update_reader'),
    path('delete-security-guard/', views.delete_security_guard, name='delete_security_guard'),
    path('update-security-guard/', views.update_security_guard, name='update_security_guard'),
    path('delete-librarian/', views.delete_librarian, name='delete_librarian'),
    path('update-librarian/', views.update_librarian, name='update_librarian'),
    path('delete-library-director/', views.delete_library_director, name='delete_library_director'),
    path('update-library-director/', views.update_library_director, name='update_library_director'),
    path('update-library-branch/', views.update_library_branch, name='update_library_branch'),
    path('delete-library-branch/', views.delete_library_branch, name='delete_library_branch'),
    path('update-book-info/', views.update_book_info, name='update_book_info'),
    path('delete-book-info/', views.delete_book_info, name='delete_book_info'),
    path('update-late-fee-info/', views.update_late_fee_info, name='update_late_fee_info'),
    path('delete-reader-faculty/', views.delete_reader_faculty, name='delete_reader_faculty'),
    path('update-reader-faculty/', views.update_reader_faculty, name='update_reader_faculty'),
    path('delete-reader-student/', views.delete_reader_student, name='delete_reader_student'),
    path('update-reader-student/', views.update_reader_student, name='update_reader_student'),
    path('update-book-location/', views.update_book_location, name='update_book_location'),
    path('return-book/', views.return_book, name='return_book'),
    path('renew-book/', views.renew_book, name='renew_book'),
    path('cancel-reservation/', views.cancel_reservation, name='cancel_reservation'),
    path('upload-book-image/', views.upload_book_image, name='upload_book_image'),
    path('upload-reader-card-photo/', views.upload_reader_card_photo, name='upload_reader_card_photo'),
    path('upload-staff-photo/', views.upload_staff_photo, name='upload_staff_photo'),
    path('get-all-borrowing-info/', views.get_all_borrowing_info, name='get_all_borrowing_info'),
    path('search-borrowing-info/', views.search_borrowing_info, name='search_borrowing_info'),
    path('get-all-reservation-info/', views.get_all_reservation_info, name='get_all_reservation_info'),
    path('search-reservation-info/', views.search_reservation_info, name='search_reservation_info'),
    path('get-all-late-fee-info/', views.get_all_late_fee_info, name='get_all_late_fee_info'),
    path('search-late-fee-info/', views.search_late_fee_info, name='search_late_fee_info'),
    path('update-late-fee-info-status/', views.update_late_fee_info_status, name='update_late_fee_info_status'),
    path('get-all-reader/', views.get_all_reader, name='get_all_reader'),
    path('search-reader/', views.search_reader, name='search_reader'),
    path('search-reader-type/', views.search_reader_type, name='search_reader_type'),
]
