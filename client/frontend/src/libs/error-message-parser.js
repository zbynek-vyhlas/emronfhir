function parseObject(message) {
  return Object.entries(message)
    .map(([key, value]) => `${key}: ${value}`)
    .join("<br>");
}

function parseString(message) {
  const regex = /<title>(.*?)<\/title>/;
  const hasTitle = message.includes("<title>") && message.includes("</title>");
  return hasTitle ? message.match(regex)[1] : message;
}

export default function errorMessageParser(message) {
  let parsedMessage = "Error message unavailable.";

  if (typeof message === "object") {
    parsedMessage = parseObject(message);
  } else if (typeof message === "string") {
    parsedMessage = parseString(message);
  }

  return parsedMessage;
}
