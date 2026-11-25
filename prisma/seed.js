const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

const sampleProducts = [
  // Pulses, Rice & Grains
  {
    productId: "SKU-1001",
    name: "Royal Basmati Rice (5kg)",
    category: "Grains & Pulses",
    quantity: 45,
    unit: "bags",
    purchasePrice: 320,
    sellingPrice: 420,
    dailySalesRate: 2.5,
    daysLeft: 60,
    supplier: "Deccan Agritech Ltd",
    storageCondition: "Dry Ambient",
  },
  {
    productId: "SKU-1002",
    name: "Toor Dal / Yellow Pulses (1kg)",
    category: "Grains & Pulses",
    quantity: 38,
    unit: "packs",
    purchasePrice: 110,
    sellingPrice: 145,
    dailySalesRate: 2.0,
    daysLeft: 45,
    supplier: "Deccan Agritech Ltd",
    storageCondition: "Dry Ambient",
  },
  {
    productId: "SKU-1003",
    name: "Moong Dal / Green Gram Pulses (1kg)",
    category: "Grains & Pulses",
    quantity: 30,
    unit: "packs",
    purchasePrice: 95,
    sellingPrice: 130,
    dailySalesRate: 1.5,
    daysLeft: 40,
    supplier: "Deccan Agritech Ltd",
    storageCondition: "Dry Ambient",
  },
  {
    productId: "SKU-1004",
    name: "Chana Dal / Bengal Gram Pulses (1kg)",
    category: "Grains & Pulses",
    quantity: 25,
    unit: "packs",
    purchasePrice: 85,
    sellingPrice: 115,
    dailySalesRate: 1.2,
    daysLeft: 35,
    supplier: "Deccan Agritech Ltd",
    storageCondition: "Dry Ambient",
  },
  {
    productId: "SKU-1005",
    name: "Whole Wheat Chakki Atta (5kg)",
    category: "Grains & Pulses",
    quantity: 40,
    unit: "bags",
    purchasePrice: 185,
    sellingPrice: 240,
    dailySalesRate: 3.0,
    daysLeft: 50,
    supplier: "Golden Mills Corp",
    storageCondition: "Dry Ambient",
  },

  // Dairy & Chilled
  {
    productId: "SKU-2001",
    name: "Fresh Cow Milk (1L)",
    category: "Dairy & Chilled",
    quantity: 24,
    unit: "bottles",
    purchasePrice: 24,
    sellingPrice: 32,
    dailySalesRate: 3.0,
    daysLeft: 3,
    supplier: "Verdant Dairies",
    storageCondition: "Chilled (2-4°C)",
  },
  {
    productId: "SKU-2002",
    name: "Whole Wheat Bread (400g)",
    category: "Bakery",
    quantity: 22,
    unit: "loaves",
    purchasePrice: 30,
    sellingPrice: 45,
    dailySalesRate: 5.0,
    daysLeft: 3,
    supplier: "Bakers Daily",
    storageCondition: "Ambient",
  },
  {
    productId: "SKU-2003",
    name: "Farm Eggs (Pack of 12)",
    category: "Dairy & Chilled",
    quantity: 50,
    unit: "crates",
    purchasePrice: 65,
    sellingPrice: 85,
    dailySalesRate: 8.0,
    daysLeft: 10,
    supplier: "Sunrise Poultry",
    storageCondition: "Chilled (10-15°C)",
  },
  {
    productId: "SKU-2004",
    name: "Fresh Malai Paneer (200g)",
    category: "Dairy & Chilled",
    quantity: 28,
    unit: "packs",
    purchasePrice: 70,
    sellingPrice: 95,
    dailySalesRate: 1.5,
    daysLeft: 4,
    supplier: "Verdant Dairies",
    storageCondition: "Chilled (2-4°C)",
  },
  {
    productId: "SKU-2005",
    name: "Greek Yogurt Berry (200g)",
    category: "Dairy & Chilled",
    quantity: 35,
    unit: "cups",
    purchasePrice: 30,
    sellingPrice: 45,
    dailySalesRate: 2.0,
    daysLeft: 4,
    supplier: "Verdant Dairies",
    storageCondition: "Chilled (2-4°C)",
  },
  {
    productId: "SKU-2006",
    name: "Salted Table Butter (500g)",
    category: "Dairy & Chilled",
    quantity: 30,
    unit: "blocks",
    purchasePrice: 42,
    sellingPrice: 58,
    dailySalesRate: 2.5,
    daysLeft: 25,
    supplier: "Verdant Dairies",
    storageCondition: "Chilled (2-4°C)",
  },
  {
    productId: "SKU-2007",
    name: "Mozzarella Cheese Block (200g)",
    category: "Dairy & Chilled",
    quantity: 20,
    unit: "blocks",
    purchasePrice: 95,
    sellingPrice: 130,
    dailySalesRate: 1.2,
    daysLeft: 7,
    supplier: "Alpine Artisan",
    storageCondition: "Chilled (2-4°C)",
  },
  {
    productId: "SKU-2008",
    name: "Fresh Cream (250ml)",
    category: "Dairy & Chilled",
    quantity: 18,
    unit: "cartons",
    purchasePrice: 48,
    sellingPrice: 65,
    dailySalesRate: 1.2,
    daysLeft: 5,
    supplier: "Verdant Dairies",
    storageCondition: "Chilled (2-4°C)",
  },
  {
    productId: "SKU-2009",
    name: "Organic Spiced Tofu (200g)",
    category: "Plant-Based",
    quantity: 18,
    unit: "packs",
    purchasePrice: 52,
    sellingPrice: 75,
    dailySalesRate: 1.0,
    daysLeft: 4,
    supplier: "Green Harvest Ltd",
    storageCondition: "Chilled (2-4°C)",
  },
  {
    productId: "SKU-2010",
    name: "Almond Unsweetened Milk (1L)",
    category: "Plant-Based",
    quantity: 15,
    unit: "tetra-paks",
    purchasePrice: 88,
    sellingPrice: 120,
    dailySalesRate: 1.0,
    daysLeft: 18,
    supplier: "Green Harvest Ltd",
    storageCondition: "Ambient",
  },
  {
    productId: "SKU-2011",
    name: "Curd Cup Classic (400g)",
    category: "Dairy & Chilled",
    quantity: 40,
    unit: "cups",
    purchasePrice: 25,
    sellingPrice: 35,
    dailySalesRate: 4.0,
    daysLeft: 5,
    supplier: "Verdant Dairies",
    storageCondition: "Chilled (2-4°C)",
  },

  // Bakery
  {
    productId: "SKU-3001",
    name: "French Butter Croissants (2pk)",
    category: "Bakery",
    quantity: 16,
    unit: "boxes",
    purchasePrice: 45,
    sellingPrice: 70,
    dailySalesRate: 1.8,
    daysLeft: 2,
    supplier: "Bakers Daily",
    storageCondition: "Ambient",
  },
  {
    productId: "SKU-3002",
    name: "Burger Buns Sesame (4pk)",
    category: "Bakery",
    quantity: 22,
    unit: "packs",
    purchasePrice: 28,
    sellingPrice: 40,
    dailySalesRate: 3.0,
    daysLeft: 4,
    supplier: "Bakers Daily",
    storageCondition: "Ambient",
  },
  {
    productId: "SKU-3003",
    name: "Chocolate Chip Muffins (2pk)",
    category: "Bakery",
    quantity: 18,
    unit: "boxes",
    purchasePrice: 40,
    sellingPrice: 60,
    dailySalesRate: 1.8,
    daysLeft: 3,
    supplier: "Bakers Daily",
    storageCondition: "Ambient",
  },
  {
    productId: "SKU-3004",
    name: "Soft Pav Buns (Pack of 6)",
    category: "Bakery",
    quantity: 26,
    unit: "packs",
    purchasePrice: 18,
    sellingPrice: 30,
    dailySalesRate: 4.5,
    daysLeft: 3,
    supplier: "Bakers Daily",
    storageCondition: "Ambient",
  },
  {
    productId: "SKU-3005",
    name: "Garlic Herb Toast Slices",
    category: "Bakery",
    quantity: 15,
    unit: "boxes",
    purchasePrice: 34,
    sellingPrice: 50,
    dailySalesRate: 1.5,
    daysLeft: 12,
    supplier: "Bakers Daily",
    storageCondition: "Dry Ambient",
  },

  // Fresh Fruits & Vegetables
  {
    productId: "SKU-4001",
    name: "Robusta Bananas (1 Dozen)",
    category: "Fresh Produce",
    quantity: 45,
    unit: "dozens",
    purchasePrice: 35,
    sellingPrice: 55,
    dailySalesRate: 5.5,
    daysLeft: 3,
    supplier: "Kisan Direct",
    storageCondition: "Ambient (18-22°C)",
  },
  {
    productId: "SKU-4002",
    name: "Sweet Strawberries Box (250g)",
    category: "Fresh Produce",
    quantity: 18,
    unit: "punnets",
    purchasePrice: 85,
    sellingPrice: 120,
    dailySalesRate: 1.2,
    daysLeft: 2,
    supplier: "Mahabaleshwar Farms",
    storageCondition: "Chilled (2-4°C)",
  },
  {
    productId: "SKU-4003",
    name: "Fresh Baby Spinach (250g)",
    category: "Fresh Produce",
    quantity: 25,
    unit: "bunches",
    purchasePrice: 14,
    sellingPrice: 25,
    dailySalesRate: 3.0,
    daysLeft: 2,
    supplier: "Kisan Direct",
    storageCondition: "Chilled misted (4°C)",
  },
  {
    productId: "SKU-4004",
    name: "White Button Mushrooms (200g)",
    category: "Fresh Produce",
    quantity: 20,
    unit: "punnets",
    purchasePrice: 38,
    sellingPrice: 55,
    dailySalesRate: 2.0,
    daysLeft: 3,
    supplier: "Green Harvest Ltd",
    storageCondition: "Chilled (2-4°C)",
  },
  {
    productId: "SKU-4005",
    name: "Organic Salad Tomatoes (1kg)",
    category: "Fresh Produce",
    quantity: 35,
    unit: "kg",
    purchasePrice: 24,
    sellingPrice: 40,
    dailySalesRate: 4.5,
    daysLeft: 5,
    supplier: "Kisan Direct",
    storageCondition: "Ambient",
  },
  {
    productId: "SKU-4006",
    name: "Shimla Red Apples (1kg)",
    category: "Fresh Produce",
    quantity: 40,
    unit: "kg",
    purchasePrice: 110,
    sellingPrice: 160,
    dailySalesRate: 3.5,
    daysLeft: 14,
    supplier: "Himachal Orchards",
    storageCondition: "Chilled (4°C)",
  },
  {
    productId: "SKU-4007",
    name: "Fresh Broccoli Crown (500g)",
    category: "Fresh Produce",
    quantity: 16,
    unit: "heads",
    purchasePrice: 42,
    sellingPrice: 65,
    dailySalesRate: 1.5,
    daysLeft: 4,
    supplier: "Green Harvest Ltd",
    storageCondition: "Chilled (2-4°C)",
  },
  {
    productId: "SKU-4008",
    name: "Sweet Nagpur Oranges (1kg)",
    category: "Fresh Produce",
    quantity: 32,
    unit: "kg",
    purchasePrice: 60,
    sellingPrice: 90,
    dailySalesRate: 3.0,
    daysLeft: 10,
    supplier: "Nagpur Citrus Co",
    storageCondition: "Ambient",
  },

  // Fresh Meat & Seafood
  {
    productId: "SKU-5001",
    name: "Boneless Chicken Breast (500g)",
    category: "Meat & Seafood",
    quantity: 14,
    unit: "trays",
    purchasePrice: 145,
    sellingPrice: 190,
    dailySalesRate: 2.5,
    daysLeft: 2,
    supplier: "Prime Cuts Ltd",
    storageCondition: "Chilled (0-2°C)",
  },
  {
    productId: "SKU-5002",
    name: "Atlantic Salmon Fillet (250g)",
    category: "Meat & Seafood",
    quantity: 10,
    unit: "fillets",
    purchasePrice: 290,
    sellingPrice: 380,
    dailySalesRate: 1.0,
    daysLeft: 2,
    supplier: "Coastal Catch",
    storageCondition: "Chilled (0-2°C)",
  },

  // Juices & Beverages
  {
    productId: "SKU-6001",
    name: "Cold Pressed Orange Juice (500ml)",
    category: "Beverages",
    quantity: 28,
    unit: "bottles",
    purchasePrice: 55,
    sellingPrice: 85,
    dailySalesRate: 2.0,
    daysLeft: 4,
    supplier: "Pure Squeeze Co",
    storageCondition: "Chilled (2-4°C)",
  },
  {
    productId: "SKU-6002",
    name: "Tender Coconut Water (200ml)",
    category: "Beverages",
    quantity: 30,
    unit: "tetra-paks",
    purchasePrice: 32,
    sellingPrice: 50,
    dailySalesRate: 4.0,
    daysLeft: 9,
    supplier: "Tropical Direct",
    storageCondition: "Ambient",
  },
  {
    productId: "SKU-6003",
    name: "Cold Brew Hazelnut Coffee (250ml)",
    category: "Beverages",
    quantity: 18,
    unit: "bottles",
    purchasePrice: 65,
    sellingPrice: 99,
    dailySalesRate: 1.5,
    daysLeft: 5,
    supplier: "Roast Master",
    storageCondition: "Chilled (2-4°C)",
  },
  {
    productId: "SKU-6004",
    name: "Alphonso Mango Smoothie (300ml)",
    category: "Beverages",
    quantity: 22,
    unit: "bottles",
    purchasePrice: 48,
    sellingPrice: 75,
    dailySalesRate: 2.0,
    daysLeft: 4,
    supplier: "Pure Squeeze Co",
    storageCondition: "Chilled (2-4°C)",
  },

  // Packaged Snacks & Staples
  {
    productId: "SKU-7001",
    name: "Digestive Wheat Biscuits (200g)",
    category: "Snacks",
    quantity: 65,
    unit: "packs",
    purchasePrice: 20,
    sellingPrice: 30,
    dailySalesRate: 4.0,
    daysLeft: 45,
    supplier: "Golden Mills Corp",
    storageCondition: "Dry Ambient",
  },
  {
    productId: "SKU-7002",
    name: "Spicy Masala Potato Chips (100g)",
    category: "Snacks",
    quantity: 50,
    unit: "packs",
    purchasePrice: 12,
    sellingPrice: 20,
    dailySalesRate: 5.0,
    daysLeft: 30,
    supplier: "Crisp Snacks Ltd",
    storageCondition: "Dry Ambient",
  },
  {
    productId: "SKU-7003",
    name: "70% Dark Cocoa Chocolate (100g)",
    category: "Confectionery",
    quantity: 35,
    unit: "bars",
    purchasePrice: 65,
    sellingPrice: 95,
    dailySalesRate: 1.5,
    daysLeft: 60,
    supplier: "Artisan Chocolatier",
    storageCondition: "Chilled (18°C)",
  },
  {
    productId: "SKU-7004",
    name: "Instant Masala Noodles (4pk)",
    category: "Packaged Staples",
    quantity: 80,
    unit: "packs",
    purchasePrice: 42,
    sellingPrice: 56,
    dailySalesRate: 7.0,
    daysLeft: 40,
    supplier: "Noodle King",
    storageCondition: "Dry Ambient",
  },
  {
    productId: "SKU-7005",
    name: "Pure Mountain Honey (250g)",
    category: "Packaged Staples",
    quantity: 25,
    unit: "jars",
    purchasePrice: 105,
    sellingPrice: 145,
    dailySalesRate: 0.8,
    daysLeft: 90,
    supplier: "Himalayan Nectar",
    storageCondition: "Ambient",
  },
];

async function main() {
  console.log("Clearing existing records...");
  await prisma.pricingRecommendation.deleteMany({});
  await prisma.alert.deleteMany({});
  await prisma.prediction.deleteMany({});
  await prisma.product.deleteMany({});
  await prisma.storeSetting.deleteMany({});

  console.log("Seeding default store settings...");
  await prisma.storeSetting.create({
    data: {
      storeName: "Inventory Analysis Supermarket",
      currency: "₹",
      highRiskThreshold: 75.0,
      mediumRiskThreshold: 45.0,
      autoDiscountEnabled: true,
      defaultDiscountPct: 20.0,
    },
  });

  console.log(`Seeding ${sampleProducts.length} authentic supermarket products...`);
  const now = new Date();

  for (const item of sampleProducts) {
    const expiry = new Date(now);
    expiry.setDate(expiry.getDate() + item.daysLeft);

    const product = await prisma.product.create({
      data: {
        productId: item.productId,
        name: item.name,
        category: item.category,
        quantity: item.quantity,
        unit: item.unit,
        purchasePrice: item.purchasePrice,
        sellingPrice: item.sellingPrice,
        stockDate: now,
        expiryDate: expiry,
        dailySalesRate: item.dailySalesRate,
        supplier: item.supplier,
        storageCondition: item.storageCondition,
      },
    });

    // Compute mathematical baseline for prediction
    const expectedSales = item.dailySalesRate * item.daysLeft;
    const leftover = Math.max(0, item.quantity - expectedSales);
    const wastageChance = Math.min(100, Math.round((leftover / Math.max(item.quantity, 1)) * 1000) / 10);
    
    let riskLevel = "Low Risk";
    let discountPct = 0;
    let action = "Healthy sales velocity; maintain standard retail pricing.";
    
    if (wastageChance >= 75) {
      riskLevel = "High Risk";
      if (item.daysLeft <= 3) {
        discountPct = 40;
        action = "Apply a 40% liquidation discount or execute return to supplier today.";
      } else if (item.daysLeft <= 7) {
        discountPct = 25;
        action = "Apply a 25% discount or bundle as a breakfast combo.";
      } else {
        discountPct = 15;
        action = "Feature in front entrance aisle with a 15% promotional tag.";
      }
    } else if (wastageChance >= 45) {
      riskLevel = "Medium Risk";
      discountPct = 10;
      action = "Keep under close watch; feature in weekly specials.";
    }

    const potentialLoss = Math.round(leftover * item.sellingPrice * 100) / 100;
    const suggestedPrice = Math.round(item.sellingPrice * (1 - discountPct / 100) * 100) / 100;
    const potentialLossAvoided = Math.round(leftover * suggestedPrice * 0.8 * 100) / 100;

    await prisma.prediction.create({
      data: {
        productId: product.id,
        daysLeft: item.daysLeft,
        expectedSales: Math.round(expectedSales * 10) / 10,
        leftover: Math.round(leftover * 10) / 10,
        wastageChance: wastageChance,
        riskLevel: riskLevel,
        potentialLoss: potentialLoss,
        recommendedAction: action,
      },
    });

    // If high risk, create alert & pricing recommendation
    if (riskLevel === "High Risk") {
      await prisma.alert.create({
        data: {
          productId: product.id,
          title: `Expiry Risk: ${item.name}`,
          message: `${item.name} has ${item.daysLeft} days left with ${item.quantity} ${item.unit} in stock. Expected leftover: ${Math.round(leftover)} units.`,
          riskLevel: "High",
        },
      });

      await prisma.pricingRecommendation.create({
        data: {
          productId: product.id,
          originalPrice: item.sellingPrice,
          suggestedPrice: suggestedPrice,
          discountPct: discountPct,
          expectedRevenue: Math.round(item.quantity * suggestedPrice),
          potentialLossAvoided: potentialLossAvoided,
          reason: `High spoilage risk with ${item.daysLeft} days before expiry. Slashing price by ${discountPct}% increases velocity by estimated 65%.`,
          status: "Pending",
        },
      });
    } else if (riskLevel === "Medium Risk") {
      await prisma.alert.create({
        data: {
          productId: product.id,
          title: `Velocity Alert: ${item.name}`,
          message: `Sales rate of ${item.dailySalesRate}/day may leave ${Math.round(leftover)} unsold units by expiry.`,
          riskLevel: "Medium",
        },
      });
    }
  }

  console.log("Database seeded successfully!");
}

main()
  .catch((e) => {
    console.error("Seed error:", e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
