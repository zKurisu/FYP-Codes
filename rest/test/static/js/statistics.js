export function drawStatisticsTable(total_statistics) {
  console.debug("Draw statistics table begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Statistics Table";
  div.appendChild(title);

  console.debug("Return drawed statistics table");
  return div
}
