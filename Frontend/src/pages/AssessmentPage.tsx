// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { motion } from 'framer-motion';
// import { ChevronRight, ChevronLeft, AlertCircle } from 'lucide-react';

// const questions = [
//   {
//     category: "Problem-Solution Fit",
//     questions: [
//       {
//         id: "q1",
//         text: "What specific problem are you solving, and why is it actually urgent right now?",
//         placeholder: "Describe the problem and its urgency...",
//         minLength: 50
//       },
//       {
//         id: "q2",
//         text: "Have you validated this with real users? (e.g., interest, usage, willingness to pay)",
//         placeholder: "Describe your validation process...",
//         minLength: 50
//       }
//     ]
//   },
//   {
//     category: "Market Opportunity",
//     questions: [
//       {
//         id: "q3",
//         text: "Who are your target customers, and how big is the market you're going after? Specify the size of competitors if any.",
//         placeholder: "Describe your target market and competition...",
//         minLength: 50
//       },
//       {
//         id: "q4",
//         text: "What makes your solution unique compared to existing alternatives?",
//         placeholder: "Describe your unique value proposition...",
//         minLength: 50
//       }
//     ]
//   },
//   {
//     category: "Execution Feasibility",
//     questions: [
//       {
//         id: "q5",
//         text: "Who's on your team, and what makes you the right people to build this?",
//         placeholder: "Describe your team's capabilities...",
//         minLength: 50
//       },
//       {
//         id: "q6",
//         text: "Do you have a clear plan or prototype for building and launching this product?",
//         placeholder: "Describe your execution plan...",
//         minLength: 50
//       }
//     ]
//   },
//   {
//     category: "Financial Feasibility",
//     questions: [
//       {
//         id: "q7",
//         text: "Do you know how much it will cost to build and launch your MVP?",
//         placeholder: "Describe your cost estimates...",
//         minLength: 50
//       },
//       {
//         id: "q8",
//         text: "How are you planning to fund it — personal funds, investors, grants?",
//         placeholder: "Describe your funding strategy...",
//         minLength: 50
//       }
//     ]
//   },
//   {
//     category: "Scalability & Sustainability",
//     questions: [
//       {
//         id: "q9",
//         text: "How will you make money (financial model), and can this grow into a large, repeatable business?",
//         placeholder: "Describe your business model...",
//         minLength: 50
//       },
//       {
//         id: "q10",
//         text: "Are there any legal, ethical, or regulatory risks you're aware of?",
//         placeholder: "Describe potential risks...",
//         minLength: 50
//       }
//     ]
//   },
//   {
//     category: "Growth Strategy",
//     questions: [
//       {
//         id: "bonus",
//         text: "How do you plan to acquire your first 100 users/customers?",
//         placeholder: "Describe your user acquisition strategy...",
//         minLength: 50
//       }
//     ]
//   }
// ];

// const AssessmentPage = () => {
//   const navigate = useNavigate();
//   const [currentSection, setCurrentSection] = useState(0);
//   const [answers, setAnswers] = useState<Record<string, string>>({});
//   const [touched, setTouched] = useState<Record<string, boolean>>({});

//   const handleAnswerChange = (questionId: string, value: string) => {
//     setAnswers(prev => ({ ...prev, [questionId]: value }));
//     setTouched(prev => ({ ...prev, [questionId]: true }));
//   };

//   const isAnswerValid = (questionId: string) => {
//     const answer = answers[questionId] || '';
//     const question = questions.flatMap(s => s.questions).find(q => q.id === questionId);
//     return answer.trim().length >= (question?.minLength || 50);
//   };

//   const isCurrentSectionComplete = () => {
//     return questions[currentSection].questions.every(q => isAnswerValid(q.id));
//   };

//   const showError = (questionId: string) => {
//     return touched[questionId] && !isAnswerValid(questionId);
//   };

//   const handleNext = () => {
//     if (currentSection < questions.length - 1) {
//       setCurrentSection(prev => prev + 1);
//       window.scrollTo(0, 0);
//     } else if (isCurrentSectionComplete()) {
//       const API_ENDPOINT = 'https://gzdbr3pf-7860.inc1.devtunnels.ms/'; // Replace with your actual endpoint
//     }
//   };

//   const handlePrevious = () => {
//     if (currentSection > 0) {
//       setCurrentSection(prev => prev - 1);
//       window.scrollTo(0, 0);
//     }
//   };

//   return (
//     <motion.div
//       initial={{ opacity: 0 }}
//       animate={{ opacity: 1 }}
//       exit={{ opacity: 0 }}
//       className="container mx-auto px-4 py-8 max-w-3xl"
//     >
//       <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-8">
//         <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
//           {questions[currentSection].category}
//         </h1>

//         <div className="space-y-6">
//           {questions[currentSection].questions.map((question) => (
//             <motion.div
//               key={question.id}
//               initial={{ y: 20, opacity: 0 }}
//               animate={{ y: 0, opacity: 1 }}
//               className="space-y-2"
//             >
//               <label className="block text-lg font-medium text-gray-700 dark:text-gray-300">
//                 {question.text}
//                 <span className="text-red-500 ml-1">*</span>
//               </label>
//               <textarea
//                 value={answers[question.id] || ''}
//                 onChange={(e) => handleAnswerChange(question.id, e.target.value)}
//                 onBlur={() => setTouched(prev => ({ ...prev, [question.id]: true }))}
//                 placeholder={question.placeholder}
//                 className={`w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white transition-colors ${
//                   showError(question.id)
//                     ? 'border-red-500 bg-red-50 dark:bg-red-900/10'
//                     : 'border-gray-300 dark:border-gray-600'
//                 }`}
//                 rows={4}
//                 required
//               />
//               {showError(question.id) && (
//                 <div className="flex items-center text-red-500 text-sm mt-1">
//                   <AlertCircle className="h-4 w-4 mr-1" />
//                   <span>Please provide a detailed answer (minimum 50 characters)</span>
//                 </div>
//               )}
//             </motion.div>
//           ))}
//         </div>

//         <div className="flex justify-between mt-8">
//           <button
//             onClick={handlePrevious}
//             disabled={currentSection === 0}
//             className={`flex items-center px-4 py-2 rounded-lg ${
//               currentSection === 0
//                 ? 'bg-gray-300 cursor-not-allowed'
//                 : 'bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600'
//             }`}
//           >
//             <ChevronLeft className="h-5 w-5 mr-2" />
//             Previous
//           </button>

//           <button
//             onClick={handleNext}
//             disabled={!isCurrentSectionComplete()}
//             className={`flex items-center px-4 py-2 rounded-lg ${
//               !isCurrentSectionComplete()
//                 ? 'bg-gray-300 cursor-not-allowed'
//                 : 'bg-blue-600 hover:bg-blue-700 text-white'
//             }`}
//           >
//             {currentSection === questions.length - 1 ? 'Submit' : 'Next'}
//             <ChevronRight className="h-5 w-5 ml-2" />
//           </button>
//         </div>
//       </div>

//       {/* Progress indicator */}
//       <div className="flex justify-center space-x-2">
//         {questions.map((_, index) => (
//           <div
//             key={index}
//             className={`h-2 w-8 rounded-full ${
//               index === currentSection
//                 ? 'bg-blue-600'
//                 : index < currentSection
//                 ? 'bg-blue-300'
//                 : 'bg-gray-300'
//             }`}
//           />
//         ))}
//       </div>
//     </motion.div>
//   );
// };

// export default AssessmentPage;
// pages/AssessmentPage.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ChevronRight, ChevronLeft, AlertCircle } from 'lucide-react';

const questions = [
  {
    category: "Problem-Solution Fit",
    questions: [
      {
        id: "q1",
        text: "What specific problem are you solving, and why is it actually urgent right now?",
        placeholder: "Describe the problem and its urgency...",
        minLength: 50
      },
      {
        id: "q2",
        text: "Have you validated this with real users? (e.g., interest, usage, willingness to pay)",
        placeholder: "Describe your validation process...",
        minLength: 50
      }
    ]
  },
  {
    category: "Market Opportunity",
    questions: [
      {
        id: "q3",
        text: "Who are your target customers, and how big is the market you're going after? Specify the size of competitors if any.",
        placeholder: "Describe your target market and competition...",
        minLength: 50
      },
      {
        id: "q4",
        text: "What makes your solution unique compared to existing alternatives?",
        placeholder: "Describe your unique value proposition...",
        minLength: 50
      }
    ]
  },
  {
    category: "Execution Feasibility",
    questions: [
      {
        id: "q5",
        text: "Who's on your team, and what makes you the right people to build this?",
        placeholder: "Describe your team's capabilities...",
        minLength: 50
      },
      {
        id: "q6",
        text: "Do you have a clear plan or prototype for building and launching this product?",
        placeholder: "Describe your execution plan...",
        minLength: 50
      }
    ]
  },
  {
    category: "Financial Feasibility",
    questions: [
      {
        id: "q7",
        text: "Do you know how much it will cost to build and launch your MVP?",
        placeholder: "Describe your cost estimates...",
        minLength: 50
      },
      {
        id: "q8",
        text: "How are you planning to fund it — personal funds, investors, grants?",
        placeholder: "Describe your funding strategy...",
        minLength: 50
      }
    ]
  },
  {
    category: "Scalability & Sustainability",
    questions: [
      {
        id: "q9",
        text: "How will you make money (financial model), and can this grow into a large, repeatable business?",
        placeholder: "Describe your business model...",
        minLength: 50
      },
      {
        id: "q10",
        text: "Are there any legal, ethical, or regulatory risks you're aware of?",
        placeholder: "Describe potential risks...",
        minLength: 50
      }
    ]
  },
  {
    category: "Growth Strategy",
    questions: [
      {
        id: "bonus",
        text: "How do you plan to acquire your first 100 users/customers?",
        placeholder: "Describe your user acquisition strategy...",
        minLength: 50
      }
    ]
  }
];

const AssessmentPage = () => {
  const navigate = useNavigate();
  const [currentSection, setCurrentSection] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const [loading, setLoading] = useState(false); // ✅

  const handleAnswerChange = (questionId: string, value: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
    setTouched(prev => ({ ...prev, [questionId]: true }));
  };

  const isAnswerValid = (questionId: string) => {
    const answer = answers[questionId] || '';
    const question = questions.flatMap(s => s.questions).find(q => q.id === questionId);
    return answer.trim().length >= (question?.minLength || 50);
  };

  const isCurrentSectionComplete = () => {
    return questions[currentSection].questions.every(q => isAnswerValid(q.id));
  };

  const showError = (questionId: string) => {
    return touched[questionId] && !isAnswerValid(questionId);
  };

  const handleNext = async () => {
    if (currentSection < questions.length - 1) {
      setCurrentSection(prev => prev + 1);
      window.scrollTo(0, 0);
    } else if (isCurrentSectionComplete()) {
      // ✅ Submit to backend and navigate to results
      setLoading(true);
      try {
        const response = await fetch('https://gzdbr3pf-7860.inc1.devtunnels.ms/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(answers),
        });

        const result = await response.json();
        navigate('/results', { state: { answers, result } }); // ✅ pass result as well if needed
      } catch (error) {
        console.error('Submission failed:', error);
        alert('Failed to submit assessment. Please try again.');
      } finally {
        setLoading(false);
      }
    }
  };

  const handlePrevious = () => {
    if (currentSection > 0) {
      setCurrentSection(prev => prev - 1);
      window.scrollTo(0, 0);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="container mx-auto px-4 py-8 max-w-3xl"
    >
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
          {questions[currentSection].category}
        </h1>

        <div className="space-y-6">
          {questions[currentSection].questions.map((question) => (
            <motion.div
              key={question.id}
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              className="space-y-2"
            >
              <label className="block text-lg font-medium text-gray-700 dark:text-gray-300">
                {question.text}
                <span className="text-red-500 ml-1">*</span>
              </label>
              <textarea
                value={answers[question.id] || ''}
                onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                onBlur={() => setTouched(prev => ({ ...prev, [question.id]: true }))}
                placeholder={question.placeholder}
                className={`w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white transition-colors ${
                  showError(question.id)
                    ? 'border-red-500 bg-red-50 dark:bg-red-900/10'
                    : 'border-gray-300 dark:border-gray-600'
                }`}
                rows={4}
                required
              />
              {showError(question.id) && (
                <div className="flex items-center text-red-500 text-sm mt-1">
                  <AlertCircle className="h-4 w-4 mr-1" />
                  <span>Please provide a detailed answer (minimum 50 characters)</span>
                </div>
              )}
            </motion.div>
          ))}
        </div>

        <div className="flex justify-between mt-8">
          <button
            onClick={handlePrevious}
            disabled={currentSection === 0}
            className={`flex items-center px-4 py-2 rounded-lg ${
              currentSection === 0
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600'
            }`}
          >
            <ChevronLeft className="h-5 w-5 mr-2" />
            Previous
          </button>

          <button
            onClick={handleNext}
            disabled={!isCurrentSectionComplete() || loading}
            className={`flex items-center px-4 py-2 rounded-lg ${
              !isCurrentSectionComplete() || loading
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            }`}
          >
            {currentSection === questions.length - 1 ? (loading ? 'Submitting...' : 'Submit') : 'Next'}
            <ChevronRight className="h-5 w-5 ml-2" />
          </button>
        </div>
      </div>

      {/* ✅ Progress indicator */}
      <div className="flex justify-center space-x-2 mt-4">
        {questions.map((_, index) => (
          <div
            key={index}
            className={`h-2 w-8 rounded-full transition-colors duration-300 ${
              index === currentSection
                ? 'bg-blue-600'
                : index < currentSection
                ? 'bg-blue-300'
                : 'bg-gray-300 dark:bg-gray-600'
            }`}
          />
        ))}
      </div>
    </motion.div>
  );
};

export default AssessmentPage;

