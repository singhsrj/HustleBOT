// import React from 'react';
// import { useLocation, useNavigate } from 'react-router-dom';
// import { motion } from 'framer-motion';
// import { CheckCircle, AlertTriangle, ArrowRight } from 'lucide-react';

// const ResultsPage = () => {
//   const location = useLocation();
//   const navigate = useNavigate();
//   const answers = location.state?.answers || {};

//   // Simple scoring logic (you can make this more sophisticated)
//   const calculateScore = () => {
//     const filledAnswers = Object.values(answers).filter(answer => answer.trim().length > 50);
//     return (filledAnswers.length / 11) * 100;
//   };

//   const score = calculateScore();

//   const getRecommendation = () => {
//     if (score >= 80) {
//       return {
//         icon: <CheckCircle className="h-12 w-12 text-green-500" />,
//         title: "Ready to Launch!",
//         message: "Your startup idea shows strong potential. Consider moving forward with development.",
//         color: "green"
//       };
//     } else if (score >= 60) {
//       return {
//         icon: <CheckCircle className="h-12 w-12 text-yellow-500" />,
//         title: "Promising with Adjustments",
//         message: "Your concept needs some refinement but shows promise. Focus on addressing the gaps identified.",
//         color: "yellow"
//       };
//     } else {
//       return {
//         icon: <AlertTriangle className="h-12 w-12 text-red-500" />,
//         title: "Needs More Work",
//         message: "Consider revisiting your core assumptions and gathering more market validation.",
//         color: "red"
//       };
//     }
//   };

//   const recommendation = getRecommendation();

//   return (
//     <motion.div
//       initial={{ opacity: 0 }}
//       animate={{ opacity: 1 }}
//       exit={{ opacity: 0 }}
//       className="container mx-auto px-4 py-8 max-w-4xl"
//     >
//       <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 mb-8">
//         <div className="text-center mb-8">
//           {recommendation.icon}
//           <h1 className="text-3xl font-bold text-gray-900 dark:text-white mt-4">
//             {recommendation.title}
//           </h1>
//           <p className="text-gray-600 dark:text-gray-400 mt-2">
//             {recommendation.message}
//           </p>
//         </div>

//         <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
//           <div className="bg-gray-50 dark:bg-gray-700 p-6 rounded-lg">
//             <h2 className="text-xl font-semibold mb-4 dark:text-white">Strengths</h2>
//             <ul className="space-y-2">
//               <li className="flex items-center text-green-600 dark:text-green-400">
//                 <CheckCircle className="h-5 w-5 mr-2" />
//                 Clear problem identification
//               </li>
//               <li className="flex items-center text-green-600 dark:text-green-400">
//                 <CheckCircle className="h-5 w-5 mr-2" />
//                 Strong market potential
//               </li>
//               <li className="flex items-center text-green-600 dark:text-green-400">
//                 <CheckCircle className="h-5 w-5 mr-2" />
//                 Viable business model
//               </li>
//             </ul>
//           </div>

//           <div className="bg-gray-50 dark:bg-gray-700 p-6 rounded-lg">
//             <h2 className="text-xl font-semibold mb-4 dark:text-white">Areas for Improvement</h2>
//             <ul className="space-y-2">
//               <li className="flex items-center text-gray-600 dark:text-gray-400">
//                 <ArrowRight className="h-5 w-5 mr-2" />
//                 Further market validation
//               </li>
//               <li className="flex items-center text-gray-600 dark:text-gray-400">
//                 <ArrowRight className="h-5 w-5 mr-2" />
//                 Detailed financial planning
//               </li>
//               <li className="flex items-center text-gray-600 dark:text-gray-400">
//                 <ArrowRight className="h-5 w-5 mr-2" />
//                 Risk mitigation strategy
//               </li>
//             </ul>
//           </div>
//         </div>

//         <div className="text-center">
//           <button
//             onClick={() => navigate('/assessment')}
//             className="bg-blue-600 text-white px-6 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
//           >
//             Retake Assessment
//           </button>
//         </div>
//       </div>
//     </motion.div>
//   );
// };

// export default ResultsPage;
import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CheckCircle, AlertTriangle, ArrowRight } from 'lucide-react';

// ✅ Score and recommendation logic moved into utils for better structure
import { calculateScore, getRecommendation } from '../utils/scoring';

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const answers = location.state?.answers || {};

  useEffect(() => {
    if (!location.state?.answers) {
      navigate('/assessment');
    }
  }, [location, navigate]);

  const score = calculateScore(answers);
  const recommendation = getRecommendation(score);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="container mx-auto px-4 py-8 max-w-4xl"
    >
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 mb-8">
        <div className="text-center mb-8">
          {recommendation.icon}
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mt-4">
            {recommendation.title}
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            {recommendation.message}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-50 dark:bg-gray-700 p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-4 dark:text-white">Strengths</h2>
            <ul className="space-y-2">
              <li className="flex items-center text-green-600 dark:text-green-400">
                <CheckCircle className="h-5 w-5 mr-2" />
                Clear problem identification
              </li>
              <li className="flex items-center text-green-600 dark:text-green-400">
                <CheckCircle className="h-5 w-5 mr-2" />
                Strong market potential
              </li>
              <li className="flex items-center text-green-600 dark:text-green-400">
                <CheckCircle className="h-5 w-5 mr-2" />
                Viable business model
              </li>
            </ul>
          </div>

          <div className="bg-gray-50 dark:bg-gray-700 p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-4 dark:text-white">Areas for Improvement</h2>
            <ul className="space-y-2">
              <li className="flex items-center text-gray-600 dark:text-gray-400">
                <ArrowRight className="h-5 w-5 mr-2" />
                Further market validation
              </li>
              <li className="flex items-center text-gray-600 dark:text-gray-400">
                <ArrowRight className="h-5 w-5 mr-2" />
                Detailed financial planning
              </li>
              <li className="flex items-center text-gray-600 dark:text-gray-400">
                <ArrowRight className="h-5 w-5 mr-2" />
                Risk mitigation strategy
              </li>
            </ul>
          </div>
        </div>

        <div className="text-center">
          <button
            onClick={() => navigate('/assessment')}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Retake Assessment
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default ResultsPage;
