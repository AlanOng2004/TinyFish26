const shortDateFormatter = new Intl.DateTimeFormat("en-SG", {
  month: "short",
  day: "numeric",
  hour: "numeric",
  minute: "2-digit",
});

const fullDateFormatter = new Intl.DateTimeFormat("en-SG", {
  dateStyle: "medium",
  timeStyle: "short",
});

const axisDateFormatter = new Intl.DateTimeFormat("en-SG", {
  month: "short",
  day: "numeric",
});

const scoreFormatter = new Intl.NumberFormat("en-US", {
  minimumFractionDigits: 1,
  maximumFractionDigits: 1,
});

const percentFormatter = new Intl.NumberFormat("en-US", {
  style: "percent",
  maximumFractionDigits: 0,
});

const relativeFormatter = new Intl.RelativeTimeFormat("en", {
  numeric: "auto",
});

function toDate(value) {
  if (!value) {
    return null;
  }

  const date = value instanceof Date ? value : new Date(value);
  return Number.isNaN(date.getTime()) ? null : date;
}

export function formatScore(value) {
  return typeof value === "number" && Number.isFinite(value)
    ? scoreFormatter.format(value)
    : "--";
}

export function formatConfidence(value) {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    return "--";
  }

  return percentFormatter.format(Math.max(0, Math.min(1, value)));
}

export function formatTimestamp(value, variant = "short") {
  const date = toDate(value);
  if (!date) {
    return "Unavailable";
  }

  return variant === "full"
    ? fullDateFormatter.format(date)
    : shortDateFormatter.format(date);
}

export function formatAxisTick(value) {
  const date = toDate(value);
  return date ? axisDateFormatter.format(date) : "";
}

export function formatRelativeTime(value) {
  const date = toDate(value);
  if (!date) {
    return "time unavailable";
  }

  const elapsed = date.getTime() - Date.now();
  const minute = 60 * 1000;
  const hour = 60 * minute;
  const day = 24 * hour;

  if (Math.abs(elapsed) >= day) {
    return relativeFormatter.format(Math.round(elapsed / day), "day");
  }

  if (Math.abs(elapsed) >= hour) {
    return relativeFormatter.format(Math.round(elapsed / hour), "hour");
  }

  return relativeFormatter.format(Math.round(elapsed / minute), "minute");
}

export function titleCaseLabel(value) {
  if (!value) {
    return "Unknown";
  }

  return String(value)
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function formatList(values, emptyLabel = "No catalysts identified yet") {
  if (!Array.isArray(values) || values.length === 0) {
    return emptyLabel;
  }

  return values.map((value) => titleCaseLabel(value)).join(" / ");
}

export function getScoreTone(score) {
  if (typeof score !== "number" || !Number.isFinite(score)) {
    return "neutral";
  }

  if (score >= 67) {
    return "positive";
  }

  if (score <= 40) {
    return "negative";
  }

  return "neutral";
}

export function getLabelTone(label) {
  const normalized = String(label ?? "").toLowerCase();

  if (normalized.includes("bullish") || normalized.includes("undervalued")) {
    return "positive";
  }

  if (normalized.includes("bearish") || normalized.includes("overvalued")) {
    return "negative";
  }

  return "neutral";
}
