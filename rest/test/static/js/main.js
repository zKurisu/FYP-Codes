import { drawFlowTable } from "./flowTable.js"
import { drawGraph } from "./graph.js"
import { drawMacToPortTable } from "./macToPortTable.js"
import { drawPortInfoTable } from "./portInfo.js"
import { drawStatisticsTable } from "./statistics.js"

const headerList = {"Prometheus": "http://127.0.0.1:5000"};
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

  Object.keys(items).forEach(key => {
    const li = document.createElement('li');
    li.textContent = key;
    
    li.addEventListener('click', () => {
      console.log("Clicked: ", key);
      fetchData(items[key])
        .then(data => {
          // 可以在这里处理返回的数据
          if (data.type == "graph") {
            console.log("I should draw a graph here")
          } else if (data.type == "flowTable") {
            console.log("I should make a flowTable here")
          } else if (data.type == "statistics") {
            console.log("I should make a statistics here")
          } else if (data.type == "portInfo") {
            console.log("I should make a portInfo here")
          } else if (data.type == "macToPortTable") {
            console.log("I should make a macToPortTable here")
          }
        })
        .catch(error => {
          // 错误处理逻辑
        });
    });

    ul.appendChild(li);
  });
  
  return ul;
}
