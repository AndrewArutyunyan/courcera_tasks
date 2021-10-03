import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def clean_data(df):
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.fillna(df.mean())
    df.iloc[:, 1::] = df.iloc[:, 1::].apply(lambda x: x*0.01)
    return df


if __name__ == '__main__':
    pd.set_option("display.max_columns", None)

    df1 = pd.read_csv('ExcelFormattedGISTEMPDataCSV.csv')
    df1 = df1.drop(columns=['J-D', 'D-N', 'DJF', 'MAM', 'JJA', 'SON'])
    df1.columns.rename("Month", inplace=True)
    df1 = clean_data(df1)
    df1 = df1.set_index('Year')

    df2 = pd.read_csv('ExcelFormattedGISTEMPData2CSV.csv')
    df2 = df2.drop(columns=['Glob', 'NHem', 'SHem'])
    df2.columns.rename("Latitude", inplace=True)
    df2 = clean_data(df2)
    cols = df2.columns[[0, 1, 4, 5, 6, 2, 7, 8, 9, 10, 11, 3]].to_list()
    df2 = df2[cols]

    print(df2)
    print(df2.columns.to_list())

    ax1 = sns.heatmap(df1.transpose(), cmap='rocket', cbar_kws={"label": "Temperature ($^\circ$C)"})
    ax1.set_ylabel("Month")

    df2_long = pd.melt(frame=df2.drop(columns="90S-64S"),
                       id_vars="Year",
                       var_name="Latitude",
                       value_name="Temperature")

    # Define the palette as a list to specify exact values
    palette = sns.color_palette("rocket_r", n_colors=len(df2.columns)-2)
    ax2 = sns.relplot(
        data=df2_long,
        x="Year", y="Temperature",
        hue="Latitude", size="Latitude", #hue_order=(df2.columns[[7,6,8,5,9,4,10,3,2,11,1]].to_list()),
        kind="line", size_order=(df2.columns[[7,6,8,5,9,4,10,3,2,11,1]].to_list()), palette=palette,
        height=5, aspect=.75, facet_kws=dict(sharex=True),row_order=[0,1,2,3,4,5,6,7,8,9,10,11],
    )
    ax2.set(ylabel="Temperature ($^\circ$C)")
    plt.show()
