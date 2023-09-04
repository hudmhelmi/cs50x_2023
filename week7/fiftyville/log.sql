-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Check crime_scene_reports for July 28, 2021, Humphrey Street
SELECT * FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Check interviews for transcript that contains bakery
SELECT * FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';

-- Check bakery_security_logs for cars leaving within 10 minutes of theft, 10.15am
SELECT * FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND activity = 'exit';

-- Check atm_transactions for Leggett Street transactions on  morning of July 28, 2021
SELECT * FROM atm_transactions
WHERE atm_location = 'Leggett Street' AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = 'withdraw';

-- Check names of account numbers
SELECT people.name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_location = 'Leggett Street' AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = 'withdraw';

-- Check phone_calls for calls on July 28, 2021 less than a minute duration
SELECT * FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60;

-- Check flights for first flight on July 29, 2021 from Fiftyville
SELECT * FROM flights
WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id IN
(
    SELECT id FROM airports
    WHERE city = 'Fiftyville'
)
ORDER BY hour, minute
LIMIT 1;

-- Find passport number from passengers
SELECT passport_number FROM passengers
WHERE flight_id IN
(
    SELECT id FROM flights
    WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id IN
    (
        SELECT id FROM airports
        WHERE city = 'Fiftyville'
    )
    ORDER BY hour, minute
    LIMIT 1
);

-- Cross reference phone_number, passport_number, license_plate, withdrew from bank at suspicious time in people
SELECT * FROM people
WHERE phone_number IN
(
    SELECT caller FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60
)
AND passport_number IN
(
    SELECT passport_number FROM passengers
    WHERE flight_id IN
    (
        SELECT id FROM flights
        WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id IN
        (
            SELECT id FROM airports
            WHERE city = 'Fiftyville'
        )
        ORDER BY hour, minute
        LIMIT 1
    )
)
AND license_plate IN
(
    SELECT license_plate FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND activity = 'exit'
)
AND name IN
(
    SELECT people.name FROM people
    JOIN bank_accounts ON bank_accounts.person_id = people.id
    JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
    WHERE atm_location = 'Leggett Street' AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = 'withdraw'
);

-- Check destination for first flight on July 29, 2021 from Fiftyville
SELECT * FROM airports WHERE id IN
(
    SELECT destination_airport_id FROM flights
    WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id IN
    (
        SELECT id FROM airports
        WHERE city = 'Fiftyville'
    )
    ORDER BY hour, minute
    LIMIT 1
);

-- Find accomplice
SELECT * FROM people
WHERE phone_number IN
(
    SELECT receiver FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60 AND caller IN
    (
        SELECT phone_number FROM people
        WHERE phone_number IN
        (
            SELECT caller FROM phone_calls
            WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60
        )
        AND passport_number IN
        (
            SELECT passport_number FROM passengers
            WHERE flight_id IN
            (
                SELECT id FROM flights
                WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id IN
                (
                    SELECT id FROM airports
                    WHERE city = 'Fiftyville'
                )
                ORDER BY hour, minute
                LIMIT 1
            )
        )
        AND license_plate IN
        (
            SELECT license_plate FROM bakery_security_logs
            WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND activity = 'exit'
        )
        AND name IN
        (
            SELECT people.name FROM people
            JOIN bank_accounts ON bank_accounts.person_id = people.id
            JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
            WHERE atm_location = 'Leggett Street' AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = 'withdraw'
        )
    )
);