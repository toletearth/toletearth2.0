-- ToletEarth — initial schema
-- Single source of truth for all property data.
-- Run via migrations/seed_db.py (creates + seeds instance/toletearth.db)

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    phone       TEXT UNIQUE NOT NULL,
    email       TEXT,
    role        TEXT NOT NULL DEFAULT 'owner',   -- owner | tenant | admin
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS cities (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS sectors (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id     INTEGER NOT NULL REFERENCES cities(id),
    name        TEXT NOT NULL,
    UNIQUE(city_id, name)
);

CREATE TABLE IF NOT EXISTS properties (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    title               TEXT NOT NULL,
    description         TEXT,
    property_type       TEXT NOT NULL DEFAULT 'Flat',   -- Flat | Builder Floor | Independent House | PG | Room
    bhk                 INTEGER NOT NULL DEFAULT 1,
    bathrooms           INTEGER NOT NULL DEFAULT 1,
    balconies           INTEGER NOT NULL DEFAULT 0,
    area_sqft           INTEGER NOT NULL DEFAULT 0,
    rent                INTEGER NOT NULL,
    security_deposit    INTEGER DEFAULT 0,

    city_id             INTEGER NOT NULL REFERENCES cities(id),
    sector_id           INTEGER NOT NULL REFERENCES sectors(id),
    address             TEXT,
    latitude            REAL,
    longitude           REAL,

    furnishing          TEXT NOT NULL DEFAULT 'Unfurnished',  -- Unfurnished | Semi-Furnished | Furnished
    parking             INTEGER NOT NULL DEFAULT 0,
    lift                INTEGER NOT NULL DEFAULT 0,
    power_backup        INTEGER NOT NULL DEFAULT 0,
    wifi                INTEGER NOT NULL DEFAULT 0,
    pet_friendly        INTEGER NOT NULL DEFAULT 0,
    bachelor_allowed    INTEGER NOT NULL DEFAULT 1,
    family_allowed      INTEGER NOT NULL DEFAULT 1,

    owner_id            INTEGER NOT NULL REFERENCES users(id),
    verified            INTEGER NOT NULL DEFAULT 0,
    featured            INTEGER NOT NULL DEFAULT 0,
    status              TEXT NOT NULL DEFAULT 'pending',  -- pending | available | rented | inactive

    created_at          TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at          TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS property_images (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id     INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    image_path      TEXT NOT NULL,
    display_order   INTEGER NOT NULL DEFAULT 0
);

-- Schema is ready for this now; UI/routes for it land in Milestone 4.
CREATE TABLE IF NOT EXISTS favourites (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    property_id     INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(user_id, property_id)
);

CREATE INDEX IF NOT EXISTS idx_properties_city ON properties(city_id);
CREATE INDEX IF NOT EXISTS idx_properties_sector ON properties(sector_id);
CREATE INDEX IF NOT EXISTS idx_properties_status ON properties(status);
CREATE INDEX IF NOT EXISTS idx_property_images_property ON property_images(property_id);
