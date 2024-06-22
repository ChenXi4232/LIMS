DELIMITER //

CREATE TRIGGER book_insert
AFTER INSERT ON book
FOR EACH ROW
BEGIN
    -- 更新分馆的馆藏书数目和图书对应索书号的现有数量和可借总数
    UPDATE bookinfo
    SET borrowable_quantity = borrowable_quantity + 1, total_quantity = total_quantity + 1
    WHERE call_number = NEW.call_number_id;
    UPDATE librarybranch
    SET book_number = book_number + 1
    WHERE branch_id = NEW.branch_location_id;
END //

-- DROP TRIGGER borrowing_insert;

CREATE TRIGGER borrowing_insert
AFTER INSERT ON borrowinginfo
FOR EACH ROW
BEGIN
    DECLARE current_status VARCHAR(10);

    -- 获取当前书本状态
    SELECT book.status INTO current_status
    FROM book
    WHERE book_id = NEW.book_id;
    -- 有预约更新预约者的取书日期
    IF current_status = 'R' THEN
        UPDATE reservationinfo
        SET pickup_date = CURDATE()
        WHERE book_id = NEW.book_id AND reader_card_id = NEW.reader_card_id AND 
        pickup_date IS NULL AND CURDATE() <= DATE_ADD(reservation_date, INTERVAL 3 DAY);
    END IF;
    -- 更新书本目前状态
    UPDATE book
    SET book.status = 'B'
    WHERE book_id = NEW.book_id;

    -- 更新读者的借书数量
    UPDATE reader
    SET borrowing_count = borrowing_count + 1
    WHERE reader_card_id = NEW.reader_card_id;
END //

-- DROP TRIGGER IF EXISTS reservation_insert;

CREATE TRIGGER reservation_insert
AFTER INSERT ON reservationinfo
FOR EACH ROW
BEGIN
    DECLARE current_status VARCHAR(10);

    -- 获取当前书本状态
    SELECT book.status INTO current_status
    FROM book
    WHERE book_id = NEW.book_id;

    -- 更新书本目前状态
    IF current_status = 'A' THEN
		UPDATE book
		SET book.status = 'R'
		WHERE book_id = NEW.book_id;
	ELSEIF current_status = 'B' THEN
		UPDATE book
		SET book.status = 'BR'
		WHERE book_id = NEW.book_id;
	END IF;
END //

CREATE TRIGGER borrow_statics
AFTER UPDATE ON book
FOR EACH ROW
BEGIN
    -- 更新图书对应索书号的现有数量和借阅总次数
    IF (OLD.status = 'A' OR OLD.status = 'R') AND NEW.status = 'B' THEN
        UPDATE bookinfo
        SET borrowing_count = borrowing_count + 1, borrowable_quantity = borrowable_quantity - 1
        WHERE call_number = NEW.call_number_id;
    END IF;
END //

-- DROP TRIGGER return_insert;

CREATE TRIGGER return_insert
AFTER UPDATE ON borrowinginfo
FOR EACH ROW
BEGIN
    DECLARE current_status VARCHAR(10);
    DECLARE overdue_days INT;
    DECLARE overdue_fine DECIMAL(10, 2);

    -- 获取当前书本状态
    SELECT book.status INTO current_status
    FROM book
    WHERE book_id = OLD.book_id;
    -- 还书后更新书本状态，读者的借书数量，图书对应索书号的现有数量
    IF OLD.return_date IS NULL AND NEW.return_date IS NOT NULL THEN
        IF current_status = 'B' THEN
            UPDATE book
            SET book.status = 'A'
            WHERE book_id = OLD.book_id;
        ELSEIF current_status = 'BR' THEN
            UPDATE book
            SET book.status = 'R'
            WHERE book_id = OLD.book_id;
        END IF;
        UPDATE reader
        SET borrowing_count = borrowing_count - 1
        WHERE reader_card_id = OLD.reader_card_id;
    END IF;
    -- 逾期还书收取罚金
    IF NEW.return_date > NEW.due_date THEN
        SET overdue_days = DATEDIFF(NEW.return_date, NEW.due_date);
        SET overdue_fine = 0.1 * overdue_days;
        UPDATE reader
        SET outstanding_amount = outstanding_amount + overdue_fine
        WHERE reader_card_id = NEW.reader_card_id;
        INSERT INTO latefeeinfo (reader_card_id, book_id, late_days, fine_amount, `status`)
        VALUES (NEW.reader_card_id, NEW.book_id, overdue_days, overdue_fine, 'Pending');
        UPDATE reader
        SET borrowing_limit = 0
        WHERE reader_card_id = NEW.reader_card_id AND outstanding_amount >= 10;
    END IF;
END //

CREATE TRIGGER return_statics
AFTER UPDATE ON book
FOR EACH ROW
BEGIN
    -- 更新图书对应索书号的现有数量
    IF (OLD.status = 'BR' OR OLD.status = 'B') AND (NEW.status = 'R' OR NEW.status = 'A') THEN
        UPDATE bookinfo
        SET borrowable_quantity = borrowable_quantity + 1
        WHERE call_number = NEW.call_number_id;
    END IF;
END //

-- 取消预约
CREATE TRIGGER reserve_cancel
AFTER DELETE ON reservationinfo
FOR EACH ROW
BEGIN
    DECLARE current_status VARCHAR(10);

    -- 获取当前书本状态
    SELECT book.status INTO current_status
    FROM book
    WHERE book_id = OLD.book_id;
    -- 更新图书状态
    IF current_status = 'R' THEN
        UPDATE book
        SET book.status = 'A'
        WHERE book_id = OLD.book_id;
    ELSEIF current_status = 'BR' THEN
        UPDATE book
        SET book.status = 'B'
        WHERE book_id = OLD.book_id;
    END IF;
END //

-- 图书移动分馆，修改分馆藏书数目
CREATE TRIGGER book_move
AFTER UPDATE ON book
FOR EACH ROW
BEGIN
    -- 更新原分馆的馆藏书数目
    IF OLD.branch_location_id IS NOT NULL THEN
        UPDATE librarybranch
        SET book_number = book_number - 1
        WHERE branch_id = OLD.branch_location_id;
    END IF;
    -- 更新新分馆的馆藏书数目
    IF NEW.branch_location_id IS NOT NULL THEN
        UPDATE librarybranch
        SET book_number = book_number + 1
        WHERE branch_id = NEW.branch_location_id;
    END IF;
END //

-- 图书删除，更新分馆的馆藏书数目和图书对应索书号的现有数量和可借总数
CREATE TRIGGER book_delete
AFTER DELETE ON book
FOR EACH ROW
BEGIN
    -- 更新分馆的馆藏书数目
    UPDATE librarybranch
    SET book_number = book_number - 1
    WHERE branch_id = OLD.branch_location_id;
    -- 更新图书对应索书号的现有数量和可借总数
    UPDATE bookinfo
    SET borrowable_quantity = borrowable_quantity - 1, total_quantity = total_quantity - 1
    WHERE call_number = OLD.call_number_id;
END //

-- 读者欠款总数根据 LateFeeInfo 表更新，status 为 'Paid' 时更新
CREATE TRIGGER update_reader_outstanding
AFTER UPDATE ON latefeeinfo
FOR EACH ROW
BEGIN
    IF NEW.status = 'Paid' AND OLD.status = 'Pending' THEN
        UPDATE reader
        SET outstanding_amount = outstanding_amount - NEW.fine_amount
        WHERE reader_card_id = NEW.reader_card_id;
    END IF;
END //

-- DROP TRIGGER remove_borrowing_limit;

-- 读者借阅限制解除触发器
CREATE TRIGGER remove_borrowing_limit
BEFORE UPDATE ON reader
FOR EACH ROW
BEGIN
    IF NEW.outstanding_amount < OLD.outstanding_amount AND NEW.outstanding_amount < 10 THEN
        SET NEW.borrowing_limit = 10;
    END IF;
END //

-- 插入 Staff 表后更新对应 branch_id 的 staff_number
CREATE TRIGGER staff_insert
AFTER INSERT ON staff
FOR EACH ROW
BEGIN
    UPDATE librarybranch
    SET staff_number = staff_number + 1
    WHERE branch_id_id = NEW.branch_id_id;
END //

-- 删除 Staff 表后更新对应 branch_id 的 staff_number
CREATE TRIGGER staff_delete
AFTER DELETE ON staff
FOR EACH ROW
BEGIN
    UPDATE librarybranch
    SET staff_number = staff_number - 1
    WHERE branch_id_id = OLD.branch_id_id;
END //

DELIMITER ;