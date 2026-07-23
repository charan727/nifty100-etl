from pathlib import Path
import sqlite3
import tempfile

import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)

from src.config import DATABASE_PATH

styles = getSampleStyleSheet()


class TearSheetGenerator:

    def __init__(self):

        self.conn = sqlite3.connect(DATABASE_PATH)

        self.output_dir = Path("reports") / "tearsheets"

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    ############################################################
    # COMPANY
    ############################################################

    def get_company(self, company_id):

        query = """
        SELECT *
        FROM companies
        WHERE id = ?
        """

        return pd.read_sql(
            query,
            self.conn,
            params=[company_id]
        )

    ############################################################
    # RATIOS
    ############################################################

    def get_ratios(self, company_id):

        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year
        """

        return pd.read_sql(
            query,
            self.conn,
            params=[company_id]
        )

    ############################################################
    # PROFIT & LOSS
    ############################################################

    def get_profit_loss(self, company_id):

        query = """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        ORDER BY year
        """

        return pd.read_sql(
            query,
            self.conn,
            params=[company_id]
        )

    ############################################################
    # BALANCE SHEET
    ############################################################

    def get_balance_sheet(self, company_id):

        query = """
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
        ORDER BY year
        """

        return pd.read_sql(
            query,
            self.conn,
            params=[company_id]
        )

    ############################################################
    # CASHFLOW
    ############################################################

    def get_cashflow(self, company_id):

        query = """
        SELECT *
        FROM cashflow
        WHERE company_id = ?
        ORDER BY year
        """

        return pd.read_sql(
            query,
            self.conn,
            params=[company_id]
        )

    ############################################################
    # PROS & CONS
    ############################################################

    def get_pros_cons(self, company_id):

        query = """
        SELECT *
        FROM prosandcons
        WHERE company_id = ?
        """

        return pd.read_sql(
            query,
            self.conn,
            params=[company_id]
        )

    ############################################################
    # LATEST ROW
    ############################################################

    def latest(self, df):

        if df.empty:
            return None

        return df.iloc[-1]

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

    def create_header(self, company):

        row = company.iloc[0]

        title = Paragraph(

            f"""
            <font size="22">
            <b>{row['company_name']}</b>
            </font>
            """,

            styles["Title"]

        )

        return title

    ############################################################
    # KPI TABLE
    ############################################################

    def create_kpi_table(self, ratios):

        latest = self.latest(ratios)

        data = [

            [

                "ROE",
                f"{self.value(latest,'return_on_equity_pct')}%",

                "ROCE",
                f"{self.value(latest,'return_on_capital_employed_pct')}%",

                "NPM",
                f"{self.value(latest,'net_profit_margin_pct')}%"

            ],

            [

                "OPM",
                f"{self.value(latest,'operating_profit_margin_pct')}%",

                "D/E",
                self.value(latest,'debt_to_equity'),

                "FCF",
                self.value(latest,'free_cash_flow_cr')

            ]

        ]

        table = Table(
            data,
            colWidths=[1.15 * inch] * 6
        )

        table.setStyle(

            TableStyle(

                [

                    ("GRID",(0,0),(-1,-1),0.5,colors.grey),

                    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#dbeafe")),

                    ("BACKGROUND",(0,1),(-1,1),colors.whitesmoke),

                    ("ALIGN",(0,0),(-1,-1),"CENTER"),

                    ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

                    ("BOTTOMPADDING",(0,0),(-1,-1),8)

                ]

            )

        )

        return table




    ###########################################################
    # REVENUE CHART
    ###########################################################

    def revenue_chart(self, pl):

        if pl.empty:
            return None

        fig, ax = plt.subplots(figsize=(5.8, 3))

        ax.bar(
            pl["year"].astype(str),
            pl["sales"]
        )

        ax.set_title("Revenue")

        ax.tick_params(axis="x", rotation=45)

        tmp = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        )

        fig.tight_layout()

        fig.savefig(
            tmp.name,
            dpi=150
        )

        plt.close(fig)

        return tmp.name


    ###########################################################
    # NET PROFIT
    ###########################################################

    def profit_chart(self, pl):

        if pl.empty:
            return None

        fig, ax = plt.subplots(figsize=(5.8, 3))

        ax.bar(
            pl["year"].astype(str),
            pl["net_profit"]
        )

        ax.set_title("Net Profit")

        ax.tick_params(axis="x", rotation=45)

        tmp = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        )

        fig.tight_layout()

        fig.savefig(
            tmp.name,
            dpi=150
        )

        plt.close(fig)

        return tmp.name


    ###########################################################
    # ROE ROCE
    ###########################################################

    def roe_roce_chart(self, ratios):

        if ratios.empty:
            return None

        fig, ax = plt.subplots(figsize=(6,3))

        ax.plot(

            ratios["year"],

            ratios["return_on_equity_pct"],

            marker="o",

            linewidth=2,

            label="ROE"

        )

        ax.plot(

            ratios["year"],

            ratios["return_on_capital_employed_pct"],

            marker="s",

            linewidth=2,

            label="ROCE"

        )

        ax.legend()

        ax.grid(True)

        ax.set_title("ROE vs ROCE")

        tmp = tempfile.NamedTemporaryFile(

            suffix=".png",

            delete=False

        )

        fig.tight_layout()

        fig.savefig(

            tmp.name,

            dpi=150

        )

        plt.close(fig)

        return tmp.name

        ###########################################################
    # BALANCE SHEET CHART
    ###########################################################

    def balance_sheet_chart(self, bs):

        if bs.empty:
            return None

        fig, ax = plt.subplots(figsize=(6, 3.5))

        years = bs["year"].astype(str)

        equity = bs["equity_capital"].fillna(0)
        reserves = bs["reserves"].fillna(0)
        borrowings = bs["borrowings"].fillna(0)

        ax.bar(
            years,
            equity,
            label="Equity"
        )

        ax.bar(
            years,
            reserves,
            bottom=equity,
            label="Reserves"
        )

        ax.bar(
            years,
            borrowings,
            bottom=equity + reserves,
            label="Borrowings"
        )

        ax.set_title("Balance Sheet Composition")

        ax.legend()

        ax.tick_params(
            axis="x",
            rotation=45
        )

        tmp = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        )

        fig.tight_layout()

        fig.savefig(
            tmp.name,
            dpi=150
        )

        plt.close(fig)

        return tmp.name


    ###########################################################
    # CASHFLOW CHART
    ###########################################################

    def cashflow_chart(self, cf):

        if cf.empty:
            return None

        fig, ax = plt.subplots(figsize=(6,3))

        years = cf["year"].astype(str)

        ax.plot(
            years,
            cf["operating_activity"],
            marker="o",
            linewidth=2,
            label="Operating"
        )

        ax.plot(
            years,
            cf["investing_activity"],
            marker="s",
            linewidth=2,
            label="Investing"
        )

        ax.plot(
            years,
            cf["financing_activity"],
            marker="^",
            linewidth=2,
            label="Financing"
        )

        ax.plot(
            years,
            cf["net_cash_flow"],
            marker="d",
            linewidth=3,
            label="Net Cash Flow"
        )

        ax.legend()

        ax.grid(True)

        ax.set_title("Cash Flow Trends")

        ax.tick_params(
            axis="x",
            rotation=45
        )

        tmp = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        )

        fig.tight_layout()

        fig.savefig(
            tmp.name,
            dpi=150
        )

        plt.close(fig)

        return tmp.name


    ###########################################################
    # PROS
    ###########################################################

    def pros_paragraph(self, df):

        if df.empty:
            return Paragraph(
                "<b>Pros</b><br/>No data available.",
                styles["BodyText"]
            )

        text = "<br/>".join(
            [
                f"• {str(x)}"
                for x in df["pros"].dropna().tolist()
            ]
        )

        return Paragraph(
            f"<b>Pros</b><br/>{text}",
            styles["BodyText"]
        )


    ###########################################################
    # CONS
    ###########################################################

    def cons_paragraph(self, df):

        if df.empty:
            return Paragraph(
                "<b>Cons</b><br/>No data available.",
                styles["BodyText"]
            )

        text = "<br/>".join(
            [
                f"• {str(x)}"
                for x in df["cons"].dropna().tolist()
            ]
        )

        return Paragraph(
            f"<b>Cons</b><br/>{text}",
            styles["BodyText"]
        )
        ###########################################################
    # GENERATE SINGLE COMPANY PDF
    ###########################################################

    def generate_company_pdf(self, company_id):

        company = self.get_company(company_id)

        if company.empty:
            return

        ratios = self.get_ratios(company_id)
        pl = self.get_profit_loss(company_id)
        bs = self.get_balance_sheet(company_id)
        cf = self.get_cashflow(company_id)
        pc = self.get_pros_cons(company_id)

        revenue_chart = self.revenue_chart(pl)
        profit_chart = self.profit_chart(pl)
        roe_chart = self.roe_roce_chart(ratios)
        bs_chart = self.balance_sheet_chart(bs)
        cf_chart = self.cashflow_chart(cf)

        company_name = company.iloc[0]["company_name"]
        company_name = (
    str(company.iloc[0]["company_name"])
    .strip()
    .replace("\n", "")
    .replace("\r", "")
    .replace("/", "-")
    .replace("\\", "-")
    .replace(":", "-")
    .replace("*", "")
    .replace("?", "")
    .replace('"', "")
    .replace("<", "")
    .replace(">", "")
    .replace("|", "")
)

        pdf_path = self.output_dir / f"{company_name}.pdf"

        doc = SimpleDocTemplate(
            str(pdf_path),
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20
        )

        story = []

        ###################################################
        # HEADER
        ###################################################

        story.append(
            self.create_header(company)
        )

        story.append(
            Spacer(1, 0.25 * inch)
        )

        ###################################################
        # KPI
        ###################################################

        story.append(
            self.create_kpi_table(ratios)
        )

        story.append(
            Spacer(1, 0.30 * inch)
        )

        ###################################################
        # REVENUE
        ###################################################

        if revenue_chart:

            story.append(
                Paragraph(
                    "<b>Revenue Trend</b>",
                    styles["Heading2"]
                )
            )

            story.append(
                Image(
                    revenue_chart,
                    width=6.5 * inch,
                    height=3.2 * inch
                )
            )

            story.append(
                Spacer(1, 0.20 * inch)
            )

        ###################################################
        # NET PROFIT
        ###################################################

        if profit_chart:

            story.append(
                Paragraph(
                    "<b>Net Profit Trend</b>",
                    styles["Heading2"]
                )
            )

            story.append(
                Image(
                    profit_chart,
                    width=6.5 * inch,
                    height=3.2 * inch
                )
            )

            story.append(
                Spacer(1, 0.20 * inch)
            )

        ###################################################
        # ROE ROCE
        ###################################################

        if roe_chart:

            story.append(
                Paragraph(
                    "<b>ROE vs ROCE</b>",
                    styles["Heading2"]
                )
            )

            story.append(
                Image(
                    roe_chart,
                    width=6.5 * inch,
                    height=3.2 * inch
                )
            )

            story.append(
                Spacer(1, 0.20 * inch)
            )

        ###################################################
        # BALANCE SHEET
        ###################################################

        if bs_chart:

            story.append(
                Paragraph(
                    "<b>Balance Sheet Composition</b>",
                    styles["Heading2"]
                )
            )

            story.append(
                Image(
                    bs_chart,
                    width=6.5 * inch,
                    height=3.2 * inch
                )
            )

            story.append(
                Spacer(1, 0.20 * inch)
            )

        ###################################################
        # CASHFLOW
        ###################################################

        if cf_chart:

            story.append(
                Paragraph(
                    "<b>Cash Flow Trend</b>",
                    styles["Heading2"]
                )
            )

            story.append(
                Image(
                    cf_chart,
                    width=6.5 * inch,
                    height=3.2 * inch
                )
            )

            story.append(
                Spacer(1, 0.20 * inch)
            )

        ###################################################
        # PAGE BREAK
        ###################################################

        story.append(
            PageBreak()
        )

        ###################################################
        # PROS
        ###################################################

        story.append(
            self.pros_paragraph(pc)
        )

        story.append(
            Spacer(1, 0.30 * inch)
        )

        ###################################################
        # CONS
        ###################################################

        story.append(
            self.cons_paragraph(pc)
        )

        doc.build(story)

        print(f"Generated : {pdf_path}")
            ###########################################################
    # GENERATE ALL TEARSHEETS
    ###########################################################

    def generate_all_tearsheets(self):

        companies = pd.read_sql(
            """
            SELECT id, company_name
            FROM companies
            ORDER BY company_name
            """,
            self.conn
        )

        total = len(companies)

        print(f"\nGenerating {total} tear sheets...\n")

        for i, row in companies.iterrows():

            try:

                print(
                    f"[{i + 1}/{total}] {row['company_name']}"
                )

                self.generate_company_pdf(
                    row["id"]
                )

            except Exception as e:

                print(
                    f"Failed : {row['company_name']}"
                )

                print(e)

        print("\nAll Tear Sheets Generated Successfully.\n")


    ###########################################################
    # CLOSE CONNECTION
    ###########################################################

    def close(self):

        if self.conn:

            self.conn.close()
            ###########################################################
# MAIN
###########################################################

if __name__ == "__main__":

    generator = TearSheetGenerator()

    try:

        generator.generate_all_tearsheets()

    finally:

        generator.close()