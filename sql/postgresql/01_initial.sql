BEGIN;

-- CreateSchema
CREATE SCHEMA IF NOT EXISTS "public";

-- CreateTable
CREATE TABLE "user" (
    "id" SERIAL NOT NULL,
    "username" TEXT,
    "password" TEXT,
    "fullname" TEXT,
    "email" TEXT,
    "address" TEXT,
    "pin_code" TEXT,
    "is_admin" BOOLEAN,

    CONSTRAINT "user_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "parking_lot" (
    "id" SERIAL NOT NULL,
    "prime_location_name" TEXT,
    "price" DOUBLE PRECISION,
    "address" TEXT,
    "pin_code" TEXT,
    "number_of_spots" INTEGER,

    CONSTRAINT "parking_lot_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "parking_spot" (
    "id" SERIAL NOT NULL,
    "lot_id" INTEGER,
    "status" TEXT,
    "spot_number" INTEGER,

    CONSTRAINT "parking_spot_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "reservation" (
    "id" SERIAL NOT NULL,
    "user_id" INTEGER,
    "spot_id" INTEGER,
    "vehicle_number" TEXT,
    "parking_timestamp" TIMESTAMP(6),
    "leaving_timestamp" TIMESTAMP(6),
    "parking_cost" DOUBLE PRECISION,
    "remarks" TEXT,

    CONSTRAINT "reservation_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "user_username_key" ON "user"("username");

-- CreateIndex
CREATE UNIQUE INDEX "user_email_key" ON "user"("email");

-- CreateIndex
CREATE UNIQUE INDEX "reservation_one_active_per_spot" ON "reservation"("spot_id") WHERE (leaving_timestamp IS NULL);

-- CreateIndex
CREATE UNIQUE INDEX "reservation_one_active_per_user" ON "reservation"("user_id") WHERE (leaving_timestamp IS NULL);

-- AddForeignKey
ALTER TABLE "parking_spot" ADD CONSTRAINT "parking_spot_lot_id_fkey" FOREIGN KEY ("lot_id") REFERENCES "parking_lot"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "reservation" ADD CONSTRAINT "reservation_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "user"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "reservation" ADD CONSTRAINT "reservation_spot_id_fkey" FOREIGN KEY ("spot_id") REFERENCES "parking_spot"("id") ON DELETE SET NULL ON UPDATE NO ACTION;

COMMIT;
