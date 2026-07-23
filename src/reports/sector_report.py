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
    PageBreak,
)

from src.config import DATABASE_PATH

styles = getSampleStyleSheet()


class SectorReportGenerator:

    def __init__(self):

        self.conn = sqlite3.connect(DATABASE_PATH)

        self.output_dir = (
            Path("reports") / "sector"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.sectors = pd.read_excel(
            "data/supporting/sectors.xlsx"
        )

    ############################################################
    # COMPANIES
    ############################################################

    def get_companies(self):

        query = """
        SELECT *
        FROM companies
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
        """

        return pd.read_sql(
            query,
            self.conn
        )

    ############################################################
    # MERGED DATA
    ############################################################

    def get_sector_data(self):

        companies = self.get_companies()

        ratios = self.get_financial_ratios()

        latest_year = ratios["year"].max()

        latest_ratios = ratios[
            ratios["year"] == latest_year
        ]

        df = companies.merge(
            self.sectors,
            left_on="id",
            right_on="company_id",
            how="left"
        )

        df = df.merge(
    latest_ratios,
    left_on="id_x",
    right_on="company_id",
    how="left",
    suffixes=("", "_ratio")
)

        return df

    ############################################################
    # SECTOR LIST
    ############################################################

    def get_sector_list(self):

        df = self.get_sector_data()

        return sorted(
            df["broad_sector"]
            .dropna()
            .unique()
            .tolist()
        )

    ############################################################
    # SINGLE SECTOR
    ############################################################

    def get_sector(self, sector_name):

        df = self.get_sector_data()

        return df[
            df["broad_sector"] == sector_name
        ].copy()

    ############################################################
    # CLOSE
    ############################################################

    def close(self):

        if self.conn:
            self.conn.close()

                ############################################################
    # MEDIAN KPI SUMMARY
    ############################################################

    def sector_summary(self, sector_df):

        if sector_df.empty:
            return None

        def median(col):

            if col not in sector_df.columns:
                return "-"

            return round(
                sector_df[col].median(),
                2
            )

        data = [

            ["Metric", "Median"],

            ["Companies", len(sector_df)],

            ["ROE %", median("return_on_equity_pct")],

            ["ROCE %", median("return_on_capital_employed_pct")],

            ["Revenue CAGR %",
             median("revenue_cagr_5yr")],

            ["PAT CAGR %",
             median("pat_cagr_5yr")],

            ["Debt / Equity",
             median("debt_to_equity")],

            ["Operating Margin %",
             median("operating_profit_margin_pct")],

            ["Free Cash Flow",
             median("free_cash_flow_cr")]

        ]

        table = Table(
            data,
            colWidths=[3.5 * inch, 2.2 * inch]
        )

        table.setStyle(

            TableStyle(

                [

                    ("GRID",(0,0),(-1,-1),0.5,colors.grey),

                    ("BACKGROUND",(0,0),(-1,0),
                     colors.HexColor("#D6EAF8")),

                    ("FONTNAME",(0,0),(-1,0),
                     "Helvetica-Bold"),

                    ("ALIGN",(0,0),(-1,-1),
                     "CENTER"),

                    ("BOTTOMPADDING",(0,0),(-1,-1),8)

                ]

            )

        )

        return table


    ############################################################
    # TOP COMPANIES
    ############################################################

    def top_companies(self, sector_df):

        if sector_df.empty:
            return []

        if "composite_quality_score" in sector_df.columns:

            top = sector_df.sort_values(

                "composite_quality_score",

                ascending=False

            ).head(5)

        elif "return_on_equity_pct" in sector_df.columns:

            top = sector_df.sort_values(

                "return_on_equity_pct",

                ascending=False

            ).head(5)

        else:

            top = sector_df.head(5)

        return top


    ############################################################
    # COMPANY TABLE
    ############################################################

    def company_table(self, sector_df):

        headers = [

            "Company",

            "ROE",

            "ROCE",

            "Rev CAGR",

            "PAT CAGR",

            "D/E",

            "OPM"

        ]

        data = [headers]

        for _, row in sector_df.iterrows():

            data.append(

                [

                    row["company_name"],

                    round(
                        row.get(
                            "return_on_equity_pct",
                            0
                        ),
                        2
                    ),

                    round(
                        row.get(
                            "return_on_capital_employed_pct",
                            0
                        ),
                        2
                    ),

                    round(
                        row.get(
                            "revenue_cagr_5yr",
                            0
                        ),
                        2
                    ),

                    round(
                        row.get(
                            "pat_cagr_5yr",
                            0
                        ),
                        2
                    ),

                    round(
                        row.get(
                            "debt_to_equity",
                            0
                        ),
                        2
                    ),

                    round(
                        row.get(
                            "operating_profit_margin_pct",
                            0
                        ),
                        2
                    )

                ]

            )

        table = Table(

            data,

            repeatRows=1,

            colWidths=[
                2.7 * inch,
                0.75 * inch,
                0.75 * inch,
                0.8 * inch,
                0.8 * inch,
                0.7 * inch,
                0.8 * inch
            ]

        )

        table.setStyle(

            TableStyle(

                [

                    ("GRID",(0,0),(-1,-1),0.25,
                     colors.grey),

                    ("BACKGROUND",(0,0),(-1,0),
                     colors.HexColor("#AED6F1")),

                    ("FONTNAME",(0,0),(-1,0),
                     "Helvetica-Bold"),

                    ("FONTSIZE",(0,0),(-1,-1),8),

                    ("BOTTOMPADDING",(0,0),(-1,0),8),

                    ("WORDWRAP",(0,0),(-1,-1),True),

                    ("VALIGN",(0,0),(-1,-1),"TOP")

                ]

            )

        )

        return table

        ############################################################
    # GENERATE SINGLE SECTOR PDF
    ############################################################

    def generate_sector_pdf(self, sector_name):

        sector_df = self.get_sector(sector_name)

        if sector_df.empty:
            return

        pdf_name = (
            sector_name
            .replace("/", "-")
            .replace("\\", "-")
            .replace(":", "")
            .replace("*", "")
            .replace("?", "")
            .replace('"', "")
            .replace("<", "")
            .replace(">", "")
            .replace("|", "")
            .strip()
        )

        pdf_path = self.output_dir / f"{pdf_name}.pdf"

        doc = SimpleDocTemplate(
            str(pdf_path),
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20
        )

        story = []

        ########################################################
        # TITLE
        ########################################################

        story.append(

            Paragraph(

                f"""
                <font size="22">
                <b>{sector_name}</b>
                </font>
                """,

                styles["Title"]

            )

        )

        story.append(
            Spacer(1, 0.30 * inch)
        )

        ########################################################
        # SUMMARY
        ########################################################

        story.append(

            Paragraph(

                "<b>Sector Summary</b>",

                styles["Heading2"]

            )

        )

        story.append(

            self.sector_summary(
                sector_df
            )

        )

        story.append(
            Spacer(1, 0.30 * inch)
        )

        ########################################################
        # TOP COMPANIES
        ########################################################

        top = self.top_companies(
            sector_df
        )

        story.append(

            Paragraph(

                "<b>Top Performers</b>",

                styles["Heading2"]

            )

        )

        for _, row in top.iterrows():

            story.append(

                Paragraph(

                    f"• {row['company_name']}",

                    styles["BodyText"]

                )

            )

        ########################################################
        # NEXT PAGE
        ########################################################

        story.append(
            PageBreak()
        )

        ########################################################
        # COMPANY TABLE
        ########################################################

        story.append(

            Paragraph(

                "<b>Companies</b>",

                styles["Heading2"]

            )

        )

        story.append(

            self.company_table(
                sector_df
            )

        )

        ########################################################
        # BUILD PDF
        ########################################################

        doc.build(story)

        print(

            f"Generated : {pdf_path}"

        )

            ############################################################
    # GENERATE ALL SECTOR REPORTS
    ############################################################

    def generate_all_sector_reports(self):

        sectors = self.get_sector_list()

        total = len(sectors)

        print(f"\nGenerating {total} Sector Reports...\n")

        for i, sector in enumerate(sectors, start=1):

            try:

                print(f"[{i}/{total}] {sector}")

                self.generate_sector_pdf(sector)

            except Exception as e:

                print(f"Failed : {sector}")

                print(e)

        print("\nAll Sector Reports Generated Successfully.\n")


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

    generator = SectorReportGenerator()

    try:

        generator.generate_all_sector_reports()

    finally:

        generator.close()