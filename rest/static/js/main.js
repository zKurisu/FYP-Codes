import { drawFlowTableCurrent } from "./flowTableCurrent.js"
import { drawFlowTableHistory } from "./flowTableHistory.js"
import { drawGraph } from "./graph.js"
import { drawMacToPortTable } from "./macToPortTable.js"
import { drawPortInfoTable } from "./portInfo.js"
import { drawStatisticsTable } from "./statistics.js"

const headerList = {"Prometheus": "http://127.0.0.1:9090"};
const contentList = {
  "Topology": "/topology",
  "Flow table history": "/flowTable/history",
  "Flow table current": "/flowTable/current",
  "Mac to port table": "/macToPortTable",
  "Port info": "/portInfo",
  "Statistics": "/statistics",
};

export function hello(name) {
  console.log(`Oh My ${name}`);
}

const fetchData = async (url) => {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const json_data = await response.json();
    console.log("Get: ", json_data);
    return json_data;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error; // 可以选择重新抛出或处理错误
  }
};

export function main(wsgi) {
  const baseUrl = wsgi.endsWith('/') ? wsgi.slice(0, -1) : wsgi;
  const headerDiv = document.getElementsByClassName("page-header")[0];
  const headerUl = make_ref_list(headerList);
  headerDiv.appendChild(headerUl);

  const contentListDiv = document.getElementsByClassName("content-list")[0];
  Object.keys(contentList).forEach(key => {
    contentList[key] = baseUrl + contentList[key];
  })
  const contentListUl = make_content_list(contentList);
  contentListDiv.appendChild(contentListUl);

  const displayBox = document.getElementsByClassName("content-display-box")[0]
  displayBox.innerHTML = "";
  fetchData(contentList["Topology"])
    .then(data => {
      let childDiv = null;
      if (data.type == "graph") {
        console.log("I should draw a graph here");
        childDiv = drawGraph(data.nodes, data.edges);
      } else {
        console.debug("Wrong type for init graph");
      }
      displayBox.appendChild(childDiv);
    })
    .catch(error => {
      console.error("Fetch error:", error);
      const errorDiv = document.createElement('div');
      errorDiv.textContent = "Error loading data";
      displayBox.appendChild(errorDiv);
    });
}

function make_ref_list(items) {
  const ul = document.createElement('ul');
  Object.keys(items).forEach(key => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = items[key];
    a.textContent = key;
    li.appendChild(a);
    ul.appendChild(li);
  })
  return ul;
}

function make_content_list(items) {
  const ul = document.createElement('ul');
  

  Object.keys(items).forEach(key => {
    const li = document.createElement('li');
    li.textContent = key;
    
    li.addEventListener('click', () => {
      console.log("Clicked: ", key);
      console.log("Clear Box..." );
      const displayBox = document.getElementsByClassName("content-display-box")[0]
      displayBox.innerHTML = "";
      fetchData(items[key])
        .then(data => {
          // 可以在这里处理返回的数据
          let childDiv = null;
          if (data.type == "graph") {
            console.log("I should draw a graph here")
            childDiv = drawGraph(data.nodes, data.edges);
          } else if (data.type == "flowTableCurrent") {
            console.log("I should make a flowTableCurrent here")
            console.debug(data["total_entities"])
            childDiv = drawFlowTableCurrent(data["total_entities"]);
          } else if (data.type == "flowTableHistory") {
            console.log("I should make a flowTableHistory here")
            console.debug(data["total_entities"])
            childDiv = drawFlowTableHistory(data["total_entities"]);
          } else if (data.type == "statistics") {
            console.log("I should make a statistics here")
            childDiv = drawStatisticsTable(data["total_statistics"]);
          } else if (data.type == "portInfo") {
            console.log("I should make a portInfo here")
            childDiv = drawPortInfoTable(data["total_port_infos"]);
          } else if (data.type == "macToPortTable") {
            console.log("I should make a macToPortTable here")
            childDiv = drawMacToPortTable(data["total_mac_to_port"]);
          }

          displayBox.appendChild(childDiv);
        })
        .catch(error => {
          console.error("Fetch error:", error);
          const errorDiv = document.createElement('div');
          errorDiv.textContent = "Error loading data";
          displayBox.appendChild(errorDiv);
        });
    });

    ul.appendChild(li);
  });
  
  return ul;
}
