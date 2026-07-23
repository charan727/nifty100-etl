from pathlib import Path
import sqlite3

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from src.config import DATABASE_PATH

styles = getSampleStyleSheet()


class PortfolioSummaryGenerator:

    def __init__(self):

        self.conn = sqlite3.connect(DATABASE_PATH)

        self.output_dir = Path("reports") / "portfolio"

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    ############################################################
    # COMPANIES
    ############################################################

    def get_companies(self):

        query = """
        SELECT *
        FROM companies
        ORDER BY company_name
        """

        return pd.read_sql(
            query,
            self.conn
        )

    ############################################################
    # FINANCIAL RATIOS
    ############################################################

    def get_financial_ratios(self):

        query = """
        SELECT *
        FROM financial_ratios
        ORDER BY company_id, year
        """

        return pd.read_sql(
            query,
            self.conn
        )

    ############################################################
    # SECTORS
    ############################################################

    def get_sectors(self):

        return pd.read_excel(
            "data/supporting/sectors.xlsx"
        )

    ############################################################
    # LATEST RATIO
    ############################################################

    def latest_ratio(self, company_id):

        ratios = self.get_financial_ratios()

        ratios = ratios[
            ratios["company_id"] == company_id
        ]

        if ratios.empty:
            return None

        return ratios.iloc[-1]

    ############################################################
    # PREVIOUS RATIO
    ############################################################

    def previous_ratio(self, company_id):

        ratios = self.get_financial_ratios()

        ratios = ratios[
            ratios["company_id"] == company_id
        ]

        if len(ratios) < 2:
            return None

        return ratios.iloc[-2]

    ############################################################
    # TREND ARROW
    ############################################################

    def trend_arrow(
        self,
        latest,
        previous,
        column
    ):

        if latest is None or previous is None:
            return "→"

        if column not in latest.index:
            return "→"

        if column not in previous.index:
            return "→"

        latest_value = latest[column]
        previous_value = previous[column]

        if pd.isna(latest_value) or pd.isna(previous_value):
            return "→"

        try:

            latest_value = float(latest_value)
            previous_value = float(previous_value)

        except Exception:

            return "→"

        difference = latest_value - previous_value

        if abs(difference) <= 2:
            return "→"

        if difference > 0:
            return "↑"

        return "↓"

    ############################################################
    # CLOSE
    ############################################################

    def close(self):

        if self.conn:
            self.conn.close()

                ############################################################
    # KPI VALUE
    ############################################################

    def value(self, row, column, default="-"):

        if row is None:
            return default

        if column not in row.index:
            return default

        value = row[column]

        if pd.isna(value):
            return default

        try:
            return round(float(value), 2)
        except Exception:
            return value


    ############################################################
    # COMPANY HEADER
    ############################################################

    def company_header(
        self,
        company,
        sector
    ):

        title = Paragraph(

            f"""
            <font size="20">
            <b>{company['company_name']}</b>
            </font>
            """,

            styles["Title"]

        )

        sector_name = sector

        if pd.isna(sector_name):
            sector_name = "-"

        subtitle = Paragraph(

            f"""
            <b>Sector :</b> {sector_name}
            <br/>
            <b>Company ID :</b> {company['id']}
            """,

            styles["Heading2"]

        )

        return title, subtitle


    ############################################################
    # KPI TABLE
    ############################################################

    def create_kpi_table(

        self,

        latest,

        previous

    ):

        data = [

            [

                "Metric",

                "Value",

                "Trend"

            ],

            [

                "ROE",

                f"{self.value(latest,'return_on_equity_pct')}%",

                self.trend_arrow(

                    latest,

                    previous,

                    "return_on_equity_pct"

                )

            ],

            [

                "ROCE",

                f"{self.value(latest,'return_on_capital_employed_pct')}%",

                self.trend_arrow(

                    latest,

                    previous,

                    "return_on_capital_employed_pct"

                )

            ],

            [

                "Revenue CAGR",

                f"{self.value(latest,'revenue_cagr_5yr')}%",

                self.trend_arrow(

                    latest,

                    previous,

                    "revenue_cagr_5yr"

                )

            ],

            [

                "PAT CAGR",

                f"{self.value(latest,'pat_cagr_5yr')}%",

                self.trend_arrow(

                    latest,

                    previous,

                    "pat_cagr_5yr"

                )

            ],

            [

                "Debt / Equity",

                self.value(

                    latest,

                    "debt_to_equity"

                ),

                self.trend_arrow(

                    latest,

                    previous,

                    "debt_to_equity"

                )

            ],

            [

                "Free Cash Flow",

                self.value(

                    latest,

                    "free_cash_flow_cr"

                ),

                self.trend_arrow(

                    latest,

                    previous,

                    "free_cash_flow_cr"

                )

            ]

        ]

        table = Table(

            data,

            colWidths=[3.2 * inch, 2 * inch, 1 * inch]

        )

        table.setStyle(

            TableStyle(

                [

                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                    ("BACKGROUND", (0, 0), (-1, 0),
                     colors.HexColor("#D6EAF8")),

                    ("FONTNAME", (0, 0), (-1, 0),
                     "Helvetica-Bold"),

                    ("ALIGN", (0, 0), (-1, -1),
                     "CENTER"),

                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8)

                ]

            )

        )

        return table

        ############################################################
    # GENERATE SINGLE COMPANY PAGE
    ############################################################

    def generate_company_page(
        self,
        story,
        company,
        sector
    ):

        latest = self.latest_ratio(
            company["id"]
        )

        previous = self.previous_ratio(
            company["id"]
        )

        title, subtitle = self.company_header(
            company,
            sector
        )

        ########################################################
        # HEADER
        ########################################################

        story.append(title)

        story.append(
            Spacer(1, 0.15 * inch)
        )

        story.append(subtitle)

        story.append(
            Spacer(1, 0.30 * inch)
        )

        ########################################################
        # KPI TABLE
        ########################################################

        story.append(

            Paragraph(

                "<b>Key Performance Indicators</b>",

                styles["Heading2"]

            )

        )

        story.append(

            self.create_kpi_table(

                latest,

                previous

            )

        )

        story.append(

            Spacer(1, 0.30 * inch)

        )

        ########################################################
        # SUMMARY
        ########################################################

        summary = f"""
        This page summarizes the latest available financial
        performance of <b>{company['company_name']}</b>.
        Trend arrows compare the latest year with the previous
        financial year.

        ↑ Improved Performance<br/>
        ↓ Declined Performance<br/>
        → Stable (within 2%)
        """

        story.append(

            Paragraph(

                summary,

                styles["BodyText"]

            )

        )

        ########################################################
        # NEXT PAGE
        ########################################################

        story.append(

            PageBreak()

        )
            ############################################################
    # GENERATE PORTFOLIO SUMMARY PDF
    ############################################################

    def generate_portfolio_summary(self):

        companies = self.get_companies()

        sectors = self.get_sectors()

        pdf_path = self.output_dir / "portfolio_summary.pdf"

        doc = SimpleDocTemplate(

            str(pdf_path),

            rightMargin=20,

            leftMargin=20,

            topMargin=20,

            bottomMargin=20

        )

        story = []

        total = len(companies)

        print(f"\nGenerating Portfolio Summary for {total} companies...\n")

        for i, (_, company) in enumerate(companies.iterrows(), start=1):

            sector_row = sectors[
                sectors["company_id"] == company["id"]
            ]

            if sector_row.empty:
                sector_name = "-"
            else:
                sector_name = sector_row.iloc[0]["broad_sector"]

            print(
                f"[{i}/{total}] {company['company_name']}"
            )

            self.generate_company_page(
                story,
                company,
                sector_name
            )

        doc.build(story)

        print(f"\nGenerated : {pdf_path}")

        print("\nPortfolio Summary Generated Successfully.\n")


    ############################################################
    # CLOSE CONNECTION
    ############################################################

    def close(self):

        if self.conn:

            self.conn.close()


############################################################
# MAIN
############################################################

if __name__ == "__main__":

    generator = PortfolioSummaryGenerator()

    try:

        generator.generate_portfolio_summary()

    finally:

        generator.close()