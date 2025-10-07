CUSTOM_PROPERTIES_MAPPING = {
    "Kurztext": ("SINGLE_LINE", "TEXT"),
    "Textfeld": ("RICH_TEXT", "TEXT"),
    "Mehrfachauswahl": ("DROPDOWN", "MULTI"),
    "Einfachauswahl": ("SINGLE_SELECT", "MULTI"),
    "Ja/Nein Auswahl": ("DROPDOWN", "YES_OR_NO"),
    "Nummer": ("PLAIN_NUMBER", "NUMBER"),
    "Nachricht": ("DROPZONE", "ATTACHMENT")
}

STANDARD_PROPERTIES_MAPPING = [
        {
            "key": "Jahresumsatz",
            "section": {
                "annualRevenueYears": [],
                "isRequired": True,
                "name": {"de": "Jahresumsatz", "en": "Annual revenues"},
                "type": "ANNUAL_REVENUES"
            }
        },
        {
            "key": "Bankverbindung",
            "section": {
                "isRequired": True,
                "name": {"de": "Bankverbindung", "en": "Bank details"},
                "type": "BANK_ACCOUNT"
            }
        },
        {
            "key": "Mitarbeiterentwicklung",
            "section": {
                "isRequired": True,
                "name": {"de": "Mitarbeiterentwicklung", "en": "Employee development"},
                "type": "EMPLOYEE_COUNTS"
            }
        },
        {
            "key": "Rechtliche Grundlagen",
            "section": {
                "isRequired": True,
                "name": {"de": "Rechtliche Grundlagen", "en": "Legal details"},
                "type": "LEGAL_DETAILS"
            }
        },
        {
            "key": "Öffentlicher Auftritt",
            "section": {
                "isRequired": True,
                "name": {"de": "Öffentlicher Auftritt", "en": "Public Appearance"},
                "type": "PUBLIC_APPEARANCE"
            }
        },
        {
            "key": "Unternehmensanschrift",
            "section": {
                "isRequired": True,
                "name": {"de": "Unternehmensanschrift", "en": "Company address"},
                "type": "SUPPLIER_INFORMATION"
            }
        },
        {
            "key": "Kontakte",
            "section": {
                "departmentIds": [],
                "name": {"de": "Kontakte", "en": "Contacts"},
                "type": "CONTACTS"
            }
        },
        {
            "key": "Investitionsvolumen",
            "section": {
                "isRequired": True,
                "name": {"de": "Investitionsvolumen", "en": "Investment volume"},
                "type": "INVESTMENTS"
            }
        },
        {
            "key": "Produktions- und Vertriebsstandorte",
            "section": {
                "isRequired": True,
                "name": {
                    "de": "Produktions- und Vertriebsstandorte",
                    "en": "Production and sales sites"
                },
                "type": "SITES"
            }
        }
    ]