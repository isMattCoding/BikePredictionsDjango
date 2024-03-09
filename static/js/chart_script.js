document.addEventListener("DOMContentLoaded", function () {
  function compareDates(a, b) {
    // Convert date strings to Date objects for comparison
    const dateA = new Date(a.date);
    const dateB = new Date(b.date);

    // Compare the dates
    if (dateA < dateB) {
      return -1;
    }
    if (dateA > dateB) {
      return 1;
    }
    return 0;
  }

  function formatDate(dateString) {
    // Create a new Date object from the dateString
    const date = new Date(dateString);

    // Specify options for formatting
    const options = {
      day: "numeric", // Numeric day of the month (e.g., 1)
      month: "short", // Abbreviated month name (e.g., Mar)
      hour: "numeric", // Numeric hour (e.g., 10)
      minute: "2-digit", // Two-digit minute (e.g., 00)
      hour12: true, // Use 12-hour clock (e.g., AM/PM)
      timeZone: "Europe/Paris", // Specify desired timezone (e.g., Paris)
    };

    // Format the date using Intl.DateTimeFormat
    return new Intl.DateTimeFormat("en-US", options).format(date);
  }

  const canvas = document.getElementById("myChart");
  const forecast_data = JSON.parse(
    canvas
      .getAttribute("data-forecast-data")
      .replace(/'/g, '"')
      .replaceAll("nan", "null")
      .replaceAll("None", "null")
  )
    .sort(compareDates)
    .map((x) => {
      return {
        date: x.DateTime,
        sum_counts: x.forecast,
        actual: typeof x.actual === "number" ? x.actual : undefined,
        lower: x.forecast_lower,
        upper: x.forecast_upper,
      };
    });
  console.log(forecast_data);
  var data = {
    labels: forecast_data.map((x) => formatDate(x.date)),
    datasets: [
      {
        label: "Bike Count per Hour",
        data: forecast_data.map((x) => x["actual"]),
        backgroundColor: "rgba(30, 130, 10, 0.2)",
        borderColor: "rgba(30, 130, 10, 1)",
        borderWidth: 1,
      },
      {
        label: "Bike forecast",
        data: forecast_data.map((x) => x["sum_counts"]),
        backgroundColor: "rgba(100, 20, 75, 0.2)",
        borderColor: "rgba(100, 20, 75, 1)",
        borderWidth: 1,
      },
      {
        label: "Upper forecast",
        data: forecast_data.map((x) => x["upper"]),
        backgroundColor: "rgba(210, 50, 135, 0.2)",
        borderColor: "rgba(210, 50, 135, 1)",
        borderWidth: 1,
      },
      {
        label: "Lower forecast",
        data: forecast_data.map((x) => x["lower"]),
        backgroundColor: "rgba(180, 30, 25, 0.2)",
        borderColor: "rgba(180, 30, 25, 1)",
        borderWidth: 1,
      },
    ],
  };
  var ctx = document.getElementById("myChart").getContext("2d");
  var myChart = new Chart(ctx, {
    type: "line",
    data: data,
  });
});
