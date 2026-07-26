from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


DATABASE_PATH = Path("db") / "nifty100.db"


class CompanyClustering:

    def __init__(self):

        self.conn = sqlite3.connect(DATABASE_PATH)

        self.output_dir = Path("output")
        self.report_dir = Path("reports")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    ############################################################
    # LOAD FINANCIAL RATIOS
    ############################################################

    def get_financial_ratios(self):

        query = """
        SELECT *
        FROM financial_ratios
        """

        return pd.read_sql(query, self.conn)

    ############################################################
    # LOAD SECTOR DATA
    ############################################################

    def get_sectors(self):

        return pd.read_excel(
            "data/supporting/sectors.xlsx"
        )

    ############################################################
    # PREPARE DATA
    ############################################################

    def prepare_data(self):

        ratios = self.get_financial_ratios()

        sectors = self.get_sectors()

        latest_year = ratios["year"].max()

        ratios = ratios[
            ratios["year"] == latest_year
        ].copy()

        df = ratios.merge(
            sectors.drop(columns=["id"]),
            on="company_id",
            how="left"
        )

        features = [
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
            "free_cash_flow_cr",
            "operating_profit_margin_pct"
        ]

        for col in features:

            df[col] = df.groupby("broad_sector")[col].transform(
                lambda x: x.fillna(x.median())
            )

        imputer = SimpleImputer(strategy="median")

        df[features] = imputer.fit_transform(
            df[features]
        )

        return df, features

        ############################################################
    # SCALE FEATURES
    ############################################################

    def scale_features(self, df, features):
        """
        Scale input features using StandardScaler.
        """

        scaler = StandardScaler()

        scaled_data = scaler.fit_transform(df[features])

        return scaled_data, scaler


    ############################################################
    # GENERATE ELBOW PLOT
    ############################################################

    def generate_elbow_plot(self, scaled_data):
        """
        Generate elbow plot for KMeans.
        """

        inertia = []

        for k in range(2, 11):

            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=10
            )

            model.fit(scaled_data)

            inertia.append(model.inertia_)

        plt.figure(figsize=(8, 5))

        plt.plot(
            range(2, 11),
            inertia,
            marker="o"
        )

        plt.title("KMeans Elbow Method")
        plt.xlabel("Number of Clusters")
        plt.ylabel("Inertia")
        plt.grid(True)

        plt.savefig(
            self.report_dir / "elbow_plot.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()


    ############################################################
    # RUN KMEANS
    ############################################################

    def run_kmeans(self, scaled_data):
        """
        Fit KMeans model.
        """

        model = KMeans(
            n_clusters=5,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(scaled_data)

        return model, labels


        ############################################################
    # ASSIGN CLUSTER NAMES
    ############################################################

    def assign_cluster_names(self, df):
        """
        Assign readable names to each cluster.
        """

        cluster_mapping = {
            0: "High-Quality Compounders",
            1: "Defensive Dividend Payers",
            2: "Value Cyclicals",
            3: "Emerging Growth",
            4: "Distressed / Turnaround"
        }

        df["cluster_name"] = df["cluster_id"].map(cluster_mapping)

        return df


    ############################################################
    # CALCULATE DISTANCE FROM CENTROID
    ############################################################

    def calculate_distance(self, model, scaled_data):

        distances = model.transform(scaled_data)

        return distances.min(axis=1)


    ############################################################
    # SAVE CLUSTER LABELS
    ############################################################

    def save_cluster_labels(self, df):

        output = df[
            [
                "company_id",
                "cluster_id",
                "cluster_name",
                "distance_from_centroid"
            ]
        ].copy()

        output.to_csv(
            self.output_dir / "cluster_labels.csv",
            index=False
        )

        print(
            f"\nCluster labels saved to: "
            f"{self.output_dir / 'cluster_labels.csv'}"
        )

        return output
    ############################################################
    # CLUSTER PROFILE
    ############################################################

    def cluster_profile(self, df, features):
        """
        Generate cluster-wise mean and median statistics.
        """

        mean_df = (
            df.groupby("cluster_name")[features]
            .mean()
            .round(2)
        )

        median_df = (
            df.groupby("cluster_name")[features]
            .median()
            .round(2)
        )

        print("\n===== Cluster Mean Profile =====")
        print(mean_df)

        print("\n===== Cluster Median Profile =====")
        print(median_df)

        return mean_df, median_df


    ############################################################
    # PORTFOLIO STATISTICS
    ############################################################

    def portfolio_statistics(self, df, features):
        """
        Generate portfolio statistics.
        """

        stats = pd.DataFrame(index=features)

        stats["Mean"] = df[features].mean()
        stats["Std"] = df[features].std()
        stats["P10"] = df[features].quantile(0.10)
        stats["P25"] = df[features].quantile(0.25)
        stats["P50"] = df[features].quantile(0.50)
        stats["P75"] = df[features].quantile(0.75)
        stats["P90"] = df[features].quantile(0.90)

        stats = stats.round(2)

        stats.to_csv(
            self.output_dir / "portfolio_stats.csv"
        )

        print("\nPortfolio statistics generated.")

        return stats
        ############################################################
    # CORRELATION HEATMAP
    ############################################################

    def correlation_heatmap(self, df, features):
        """
        Generate correlation heatmap.
        """

        correlation = df[features].corr(method="pearson")

        plt.figure(figsize=(8, 6))

        plt.imshow(
            correlation,
            cmap="coolwarm",
            interpolation="nearest"
        )

        plt.colorbar()

        plt.xticks(
            range(len(features)),
            features,
            rotation=45,
            ha="right"
        )

        plt.yticks(
            range(len(features)),
            features
        )

        plt.title("Correlation Heatmap")

        plt.tight_layout()

        plt.savefig(
            self.report_dir / "correlation_heatmap.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("\nCorrelation Heatmap Generated.")

        ############################################################
    # RUN COMPLETE PIPELINE
    ############################################################

    def run(self):

        print("\nStarting Company Clustering...")

        df, features = self.prepare_data()

        scaled_data, scaler = self.scale_features(
            df,
            features
        )

        self.generate_elbow_plot(
            scaled_data
        )

        model, labels = self.run_kmeans(
            scaled_data
        )

        df["cluster_id"] = labels

        df = self.assign_cluster_names(df)

        df["distance_from_centroid"] = self.calculate_distance(
            model,
            scaled_data
        )

        self.save_cluster_labels(df)
        self.cluster_profile(
            df,
            features
        )

        self.portfolio_statistics(
            df,
            features
        )

        self.correlation_heatmap(
            df,
            features
        )

        print("\nDay 36 completed successfully.")

        # self.close()

            ############################################################
    # CLOSE DATABASE
    ############################################################

    def close(self):
        if self.conn:
            self.conn.close()


############################################################
# MAIN
############################################################

if __name__ == "__main__":

    clustering = CompanyClustering()

    clustering.run()


        ############################################################
    # CLOSE DATABASE
    ############################################################

    def close(self):

        if self.conn:

            self.conn.close()