import { Waves, Wifi, Dumbbell, Coffee, Sparkles, Car, UtensilsCrossed, Wine, Plane, PawPrint, ConciergeBell, Presentation, Check } from "lucide-react";

export const GRADIENTS = [
  "linear-gradient(135deg,#1a1635 0%,#2d1f4a 100%)",
  "linear-gradient(135deg,#0f2a1a 0%,#1a3d2b 100%)",
  "linear-gradient(135deg,#1a1a2e 0%,#16213e 100%)",
  "linear-gradient(135deg,#2a1a0f 0%,#3d2b1a 100%)",
  "linear-gradient(135deg,#1a1a1a 0%,#2d2d2d 100%)",
  "linear-gradient(135deg,#1a1228 0%,#2a1a3d 100%)",
  "linear-gradient(135deg,#0d1f2a 0%,#1a3040 100%)",
  "linear-gradient(135deg,#1f1a0d 0%,#302a1a 100%)",
];

const AMENITY_ICONS = {
  "Swimming Pool": Waves, "Free WiFi": Wifi, "Gym": Dumbbell, "Breakfast": Coffee,
  "Spa": Sparkles, "Parking": Car, "Restaurant": UtensilsCrossed, "Bar": Wine,
  "Airport Shuttle": Plane, "Pet Friendly": PawPrint, "Room Service": ConciergeBell, "Conference": Presentation,
};

export function amenityIcon(a, size = 14) {
  const Icon = AMENITY_ICONS[a];
  return Icon ? <Icon size={size} /> : <Check size={size} />;
}
