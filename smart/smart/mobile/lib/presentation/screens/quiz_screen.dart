import 'package:flutter/material.dart';
import 'dart:async';

class QuizScreen extends StatefulWidget {
  const QuizScreen({super.key});

  @override
  State<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  int _currentQuestionIndex = 0;
  int _timeLeft = 600; // 10 minutes in seconds
  Timer? _timer;
  
  // Mock Data
  final List<Map<String, Object>> _questions = [
    {
      'question': 'What is the unit of Force?',
      'options': ['Newton', 'Watt', 'Joule', 'Pascal'],
      'answer': 0
    },
    {
      'question': 'Which planet is known as the Red Planet?',
      'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
      'answer': 1
    },
  ];

  @override
  void initState() {
    super.initState();
    _startTimer();
  }

  void _startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_timeLeft > 0) {
        setState(() {
          _timeLeft--;
        });
      } else {
        _timer?.cancel();
        _submitQuiz();
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _submitQuiz() {
    showDialog(
      context: context, 
      builder: (ctx) => AlertDialog(
        title: const Text('Quiz Completed'),
        content: const Text('Your answers have been saved locally. Results will sync when online.'),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(ctx).pop(); // Close dialog
              Navigator.of(context).pop(); // Go back to dashboard
            }, 
            child: const Text('OK')
          )
        ],
      )
    );
  }

  String get _formattedTime {
    final minutes = (_timeLeft / 60).floor();
    final seconds = _timeLeft % 60;
    return '${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    if (_currentQuestionIndex >= _questions.length) {
       return Scaffold(
         body: Center(child: CircularProgressIndicator()),
       );
    }
    
    final question = _questions[_currentQuestionIndex];
    final options = question['options'] as List<String>;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Practice Quiz'),
        actions: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: Center(
              child: Text(
                _formattedTime,
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ),
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            LinearProgressIndicator(
              value: (_currentQuestionIndex + 1) / _questions.length,
            ),
            const SizedBox(height: 20),
            Text(
              'Question ${_currentQuestionIndex + 1}/${_questions.length}',
              style: const TextStyle(color: Colors.grey),
            ),
            const SizedBox(height: 10),
            Text(
              question['question'] as String,
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 30),
            ...options.asMap().entries.map((entry) {
              return Padding(
                padding: const EdgeInsets.only(bottom: 12.0),
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.all(16),
                    alignment: Alignment.centerLeft,
                    textStyle: const TextStyle(fontSize: 16),
                  ),
                  onPressed: () {
                    if (_currentQuestionIndex < _questions.length - 1) {
                      setState(() {
                        _currentQuestionIndex++;
                      });
                    } else {
                      _submitQuiz();
                    }
                  },
                  child: Text('${String.fromCharCode(65 + entry.key)}. ${entry.value}'),
                ),
              );
            }).toList(),
          ],
        ),
      ),
    );
  }
}
