-- CreateTable
CREATE TABLE `user` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(512) NULL,
    `password` TEXT NULL,
    `fullname` TEXT NULL,
    `email` VARCHAR(512) NULL,
    `address` TEXT NULL,
    `pin_code` TEXT NULL,
    `is_admin` BOOLEAN NULL,

    UNIQUE INDEX `user_username_key`(`username`),
    UNIQUE INDEX `user_email_key`(`email`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin;

-- CreateTable
CREATE TABLE `parking_lot` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `prime_location_name` TEXT NULL,
    `price` DOUBLE NULL,
    `address` TEXT NULL,
    `pin_code` TEXT NULL,
    `number_of_spots` INTEGER NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin;

-- CreateTable
CREATE TABLE `parking_spot` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `lot_id` INTEGER NULL,
    `status` TEXT NULL,
    `spot_number` INTEGER NULL,

    INDEX `parking_spot_lot_id_fkey`(`lot_id`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin;

-- CreateTable
CREATE TABLE `reservation` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `user_id` INTEGER NULL,
    `spot_id` INTEGER NULL,
    `vehicle_number` TEXT NULL,
    `parking_timestamp` DATETIME(6) NULL,
    `leaving_timestamp` DATETIME(6) NULL,
    `parking_cost` DOUBLE NULL,
    `remarks` TEXT NULL,

    INDEX `reservation_user_id_fkey`(`user_id`),
    INDEX `reservation_spot_id_fkey`(`spot_id`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin;

-- CreateTable
CREATE TABLE `reservation_audit` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `reservation_id` INTEGER NOT NULL,
    `event_type` TEXT NOT NULL,
    `recorded_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `final_cost` DOUBLE NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin;

-- AddForeignKey
ALTER TABLE `parking_spot` ADD CONSTRAINT `parking_spot_lot_id_fkey` FOREIGN KEY (`lot_id`) REFERENCES `parking_lot`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- AddForeignKey
ALTER TABLE `reservation` ADD CONSTRAINT `reservation_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- AddForeignKey
ALTER TABLE `reservation` ADD CONSTRAINT `reservation_spot_id_fkey` FOREIGN KEY (`spot_id`) REFERENCES `parking_spot`(`id`) ON DELETE SET NULL ON UPDATE RESTRICT;
