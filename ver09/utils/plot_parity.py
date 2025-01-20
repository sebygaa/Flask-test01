import matplotlib.pyplot as plt

def plot_parity(y_true, y_pred, output_columns):
    """
    Generates parity plots for true vs predicted values.

    Args:
        y_true (pd.DataFrame): True output values.
        y_pred (pd.DataFrame): Predicted output values.
        output_columns (list): List of output column names.

    Returns:
        str: Path to the saved parity plot image.
    """
    num_outputs = len(output_columns)
    plt.figure(figsize=(8, 6 * num_outputs))

    for i, col in enumerate(output_columns):
        plt.subplot(num_outputs, 1, i + 1)
        plt.scatter(y_true[col], y_pred[col], alpha=0.7, label=f"{col} (True vs Predicted)")
        plt.plot([y_true[col].min(), y_true[col].max()], 
                 [y_true[col].min(), y_true[col].max()], 
                 color='red', linestyle='--', label="Perfect Parity")
        plt.xlabel("True Values")
        plt.ylabel("Predicted Values")
        plt.title(f"Parity Plot for {col}")
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plot_path = "static/parity_plot.png"
    plt.savefig(plot_path)
    plt.close()

    return plot_path
