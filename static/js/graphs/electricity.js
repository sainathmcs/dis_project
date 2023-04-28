const chartName = "electricityChart";

setTimeout(() => {
  let xValues = [
    "Front Door Camera",
    "Light",
    "Bulb",
    "Thermostat",
    "Amazon Alexa",
  ];
  let yValues = [55, 49, 44, 24, 15];
  let barColors = ["red", "green", "blue", "orange", "brown"];

  new Chart(chartName, {
    type: "bar",
    data: {
      labels: xValues,
      datasets: [
        {
          backgroundColor: barColors,
          data: yValues,
        },
      ],
    },
    options: {},
  });
}, 1000);
