class Question {
  final String id;
  final String question;
  final Map<String, String> options;
  final int correctAnswerIndex;
  final String explanation;
  final String subject;
  final String topic;
  
  Question({
    required this.id,
    required this.question,
    required this.options,
    required this.correctAnswerIndex,
    required this.explanation,
    required this.subject,
    required this.topic,
  });
  
  factory Question.fromJson(Map<String, dynamic> json) {
    return Question(
      id: json['id'] ?? '',
      question: json['question'] ?? '',
      options: Map<String, String>.from(json['options'] ?? {}),
      correctAnswerIndex: json['correct_answer_index'] ?? 0,
      explanation: json['explanation'] ?? '',
      subject: json['subject'] ?? '',
      topic: json['topic'] ?? '',
    );
  }
  
  String get correctAnswer {
    final keys = options.keys.toList();
    if (correctAnswerIndex < keys.length) {
      return options[keys[correctAnswerIndex]] ?? '';
    }
    return '';
  }
}
