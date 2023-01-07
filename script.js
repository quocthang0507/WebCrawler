let data = [];
const parent = 'body',
  selector = `${parent}, ${parent} *:not(style, script)`,
  elements = [...document.querySelectorAll(selector)];
elements.forEach(element => {
  element.childNodes.forEach(node => {
    const text = node && node.nodeType != 8 && node.nodeValue;
    if (text && /\S/.test(text) && text.length > 1 && !/^\d+$/.test(text)) {
      data.push(text.trim());
    }
  });
});
data = [...new Set(data)];
return data;