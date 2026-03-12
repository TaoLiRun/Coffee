# This script provides visualization functions for demand analysis, including daily demand by store, 
# product demand trends, and the impact of product changes on demand patterns.

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def visualize_consumer_new_product_curve(stats_df, output_folder='plots'):
    """
    Visualize how many consumers purchase a new product at each purchase index.
    stats_df columns: purchase_idx, new_count, total, ratio
    """
    os.makedirs(output_folder, exist_ok=True)
    stats_df = stats_df.sort_values("purchase_idx")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(stats_df["purchase_idx"], stats_df["new_count"], color="steelblue", alpha=0.7, label="New product count")
    ax2 = ax.twinx()
    ax2.plot(stats_df["purchase_idx"], stats_df["ratio"], color="coral", linewidth=2, marker="o", label="Ratio new")

    ax.set_xlabel("Purchase index", fontsize=12)
    ax.set_ylabel("Number of consumers (new product)", fontsize=12)
    ax2.set_ylabel("Ratio of new product", fontsize=12)
    ax.set_title("New Product Adoption by Purchase Index", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")

    plt.tight_layout()
    output_path = os.path.join(output_folder, "consumer_new_product_curve.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved new product curve plot to: {output_path}")
    plt.close()
    return output_path


def visualize_immediate_repurchase_rate(rate_df, output_folder='plots'):
    """
    Visualize immediate repurchase rate vs purchase index.
    rate_df columns: purchase_idx, immediate_repurchase_rate
    """
    os.makedirs(output_folder, exist_ok=True)
    rate_df = rate_df.sort_values("purchase_idx")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(rate_df["purchase_idx"], rate_df["immediate_repurchase_rate"],
            marker="o", linewidth=2, color="purple")
    ax.set_xlabel("Purchase index", fontsize=12)
    ax.set_ylabel("Immediate repurchase rate", fontsize=12)
    ax.set_title("Immediate Repurchase Rate by Purchase Index", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1)

    plt.tight_layout()
    output_path = os.path.join(output_folder, "consumer_immediate_repurchase_rate.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved immediate repurchase rate plot to: {output_path}")
    plt.close()
    return output_path

