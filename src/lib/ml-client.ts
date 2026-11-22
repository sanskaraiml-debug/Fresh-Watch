export interface ItemPredictInput {
  product: string;
  stock: number;
  daily_sales: number;
  days_left: number;
  price?: number;
  category?: string;
}

export interface PredictionResult {
  product: string;
  category: string;
  stock: number;
  daily_sales: number;
  days_left: number;
  price: number;
  expected_sales: number;
  unsold_quantity: number;
  potential_loss: number;
  wastage_chance: number;
  risk_level: "High Risk" | "Medium Risk" | "Low Risk";
  discount_pct: number;
  suggested_price: number;
  recommended_action: string;
  is_ml_service?: boolean;
}

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || "http://127.0.0.1:8000";

/**
 * Calculates mathematical prediction fallback if FastAPI service is unreachable
 */
function localFallbackPrediction(input: ItemPredictInput): PredictionResult {
  const stock = Number(input.stock);
  const daily_sales = Number(input.daily_sales);
  const days_left = Number(input.days_left);
  const price = Number(input.price || 0);

  const expected_sales = Math.round(daily_sales * days_left * 10) / 10;
  const leftover = Math.max(0, Math.round((stock - expected_sales) * 10) / 10);
  const ratio = stock > 0 ? leftover / stock : 0;
  const wastage_chance = Math.min(100, Math.round(ratio * 1000) / 10);

  let risk_level: "High Risk" | "Medium Risk" | "Low Risk" = "Low Risk";
  let discount_pct = 0;
  let action = "Healthy sales velocity; maintain standard retail pricing.";

  if (wastage_chance >= 75) {
    risk_level = "High Risk";
    if (days_left <= 3) {
      discount_pct = 40;
      action = "Give a 40% liquidation discount or execute return to supplier today";
    } else if (days_left <= 7) {
      discount_pct = 25;
      action = "Apply a 20-30% discount or create a promotional combo offer";
    } else {
      discount_pct = 15;
      action = "Move to eye-level front shelf and apply a 10-15% markdown";
    }
  } else if (wastage_chance >= 45) {
    risk_level = "Medium Risk";
    discount_pct = 10;
    action = "Keep under close watch; feature in weekly specials";
  }

  const unsold_quantity = leftover;
  const potential_loss = Math.round(unsold_quantity * price * 100) / 100;
  const suggested_price = Math.round(price * (1 - discount_pct / 100) * 100) / 100;

  return {
    product: input.product,
    category: input.category || "General",
    stock,
    daily_sales,
    days_left,
    price,
    expected_sales,
    unsold_quantity,
    potential_loss,
    wastage_chance,
    risk_level,
    discount_pct,
    suggested_price,
    recommended_action: action,
    is_ml_service: false,
  };
}

export async function predictSingle(input: ItemPredictInput): Promise<PredictionResult> {
  try {
    const res = await fetch(`${ML_SERVICE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input),
      // short timeout so we fallback gracefully
      signal: AbortSignal.timeout(2000),
    });

    if (res.ok) {
      const data = await res.json();
      return { ...data, is_ml_service: true };
    }
  } catch (err) {
    // console.warn("ML microservice offline, using local inference:", err);
  }

  return localFallbackPrediction(input);
}

export async function predictBatch(items: ItemPredictInput[]): Promise<{
  total_items: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  total_potential_loss: number;
  predictions: PredictionResult[];
}> {
  try {
    const res = await fetch(`${ML_SERVICE_URL}/batch-predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items }),
      signal: AbortSignal.timeout(4000),
    });

    if (res.ok) {
      const data = await res.json();
      return data;
    }
  } catch (err) {
    // Fallback batch
  }

  const predictions = items.map(localFallbackPrediction);
  const high_risk_count = predictions.filter((p) => p.risk_level === "High Risk").length;
  const medium_risk_count = predictions.filter((p) => p.risk_level === "Medium Risk").length;
  const low_risk_count = predictions.filter((p) => p.risk_level === "Low Risk").length;
  const total_potential_loss = predictions.reduce((acc, p) => acc + p.potential_loss, 0);

  return {
    total_items: items.length,
    high_risk_count,
    medium_risk_count,
    low_risk_count,
    total_potential_loss: Math.round(total_potential_loss * 100) / 100,
    predictions,
  };
}
