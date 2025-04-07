import { CheckCircle, AlertTriangle } from 'lucide-react';

export const calculateScore = (answers: Record<string, string>) => {
  const filledAnswers = Object.values(answers).filter(ans => ans.trim().length >= 50);
  return (filledAnswers.length / 11) * 100;
};

export const getRecommendation = (score: number) => {
  if (score >= 80) {
    return {
      icon: <CheckCircle className="h-12 w-12 text-green-500" />,
      title: "Ready to Launch!",
      message: "Your startup idea shows strong potential. Consider moving forward with development.",
      color: "green",
    };
  } else if (score >= 60) {
    return {
      icon: <CheckCircle className="h-12 w-12 text-yellow-500" />,
      title: "Promising with Adjustments",
      message: "Your concept needs some refinement but shows promise. Focus on addressing the gaps identified.",
      color: "yellow",
    };
  } else {
    return {
      icon: <AlertTriangle className="h-12 w-12 text-red-500" />,
      title: "Needs More Work",
      message: "Consider revisiting your core assumptions and gathering more market validation.",
      color: "red",
    };
  }
};
