BEGIN;

CREATE TABLE "reservation_audit" (
    "id" SERIAL NOT NULL,
    "reservation_id" INTEGER NOT NULL,
    "event_type" TEXT NOT NULL,
    "recorded_at" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "final_cost" DOUBLE PRECISION,
    CONSTRAINT "reservation_audit_pkey" PRIMARY KEY ("id")
);

CREATE FUNCTION public.record_reservation_release() RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO public.reservation_audit (reservation_id, event_type, final_cost)
    VALUES (NEW.id, 'RELEASED', NEW.parking_cost);
    RETURN NEW;
END;
$$;

CREATE TRIGGER reservation_release_audit
AFTER UPDATE OF leaving_timestamp ON "reservation"
FOR EACH ROW
WHEN (OLD.leaving_timestamp IS NULL AND NEW.leaving_timestamp IS NOT NULL)
EXECUTE FUNCTION public.record_reservation_release();

COMMIT;
