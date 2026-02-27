class User {
  final String id;
  final String username;
  final String email;
  final String language;

  User({
    required this.id,
    required this.username,
    required this.email,
    this.language = 'en',
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['_id'] ?? json['id'] ?? '',
      username: json['username'] ?? '',
      email: json['email'] ?? '',
      language: json['language'] ?? 'en',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'language': language,
    };
  }
}
