-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Prediction" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "patientId" TEXT NOT NULL,
    "filePath" TEXT NOT NULL,
    "prediction" TEXT NOT NULL,
    "confidence" REAL NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "Prediction_patientId_fkey" FOREIGN KEY ("patientId") REFERENCES "Patient" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO "new_Prediction" ("confidence", "createdAt", "filePath", "id", "patientId", "prediction") SELECT "confidence", "createdAt", "filePath", "id", "patientId", "prediction" FROM "Prediction";
DROP TABLE "Prediction";
ALTER TABLE "new_Prediction" RENAME TO "Prediction";
CREATE TABLE "new_EEGRecord" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "fileName" TEXT NOT NULL,
    "filePath" TEXT NOT NULL,
    "patientId" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "EEGRecord_patientId_fkey" FOREIGN KEY ("patientId") REFERENCES "Patient" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO "new_EEGRecord" ("createdAt", "fileName", "filePath", "id", "patientId", "userId") SELECT "createdAt", "fileName", "filePath", "id", "patientId", "userId" FROM "EEGRecord";
DROP TABLE "EEGRecord";
ALTER TABLE "new_EEGRecord" RENAME TO "EEGRecord";
PRAGMA foreign_key_check("Prediction");
PRAGMA foreign_key_check("EEGRecord");
PRAGMA foreign_keys=ON;
