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

  function formatDate(dateString, index) {
    // Create a new Date object from the dateString
    const date = new Date(dateString);

    // Specify options for formatting
    const options = {
      day: "numeric", // Numeric day of the month (e.g., 1)
      month: "short", // Abbreviated month name (e.g., Mar)
      hour: "numeric", // Numeric hour (e.g., 10)
      hour12: true, // Use 12-hour clock (e.g., AM/PM)
      timeZone: "Europe/Paris", // Specify desired timezone (e.g., Paris)
    };

    // Format the date using Intl.DateTimeFormat
    const formattedDate = new Intl.DateTimeFormat("en-GB", options).format(
      date
    );
    console.log(formattedDate);
    if (formattedDate.includes("12 AM") || index === 0) {
      return formattedDate;
    }
    return formattedDate.split(", ")[1];
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
        forecast: x.forecast,
        actual: typeof x.actual === "number" ? x.actual : undefined,
        lower: x.forecast_lower,
        upper: x.forecast_upper,
      };
    });
  const sliced_forecast_data = forecast_data.slice(40, 72);
  var data = {
    labels: sliced_forecast_data.map((x, index) => formatDate(x.date, index)),
    datasets: [
      {
        label: "Bike Count per Hour",
        data: sliced_forecast_data.map((x) => x["actual"]),
        backgroundColor: "rgba(255, 99, 71, 0.2)",
        borderColor: "rgba(255, 99, 71, 1)",
        borderWidth: 1,
      },
      {
        label: "Bike forecast",
        data: sliced_forecast_data.map((x) => x["forecast"]),
        backgroundColor: "rgba(65, 105, 225, 0.2)",
        borderColor: "rgba(65, 105, 225, 0.8)",
        borderWidth: 1,
      },
      {
        label: "Upper forecast",
        data: sliced_forecast_data.map((x) => x["upper"]),
        backgroundColor: "rgba(0, 128, 0, 0.2)",
        borderColor: "rgba(0, 128, 0, 0.6)",
        borderWidth: 1,
      },
      {
        label: "Lower forecast",
        data: sliced_forecast_data.map((x) => x["lower"]),
        backgroundColor: "rgba(0, 128, 0, 0.2)",
        borderColor: "rgba(0, 128, 0, 0.6)",
        borderWidth: 1,
      },
    ],
  };
  var ctx = document.getElementById("myChart").getContext("2d");
  var myChart = new Chart(ctx, {
    type: "line",
    data: data,
    options: {
      scales: {
        y: {
          min: 0,
          ticks: {
            stepSize: 200,
          },
        },
        x: {
          ticks: {
            stepSize: 2,
          },
        },
      },
    },
  });
  console.log(myChart);
});
