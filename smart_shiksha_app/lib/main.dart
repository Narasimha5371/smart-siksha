import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:provider/provider.dart';
import 'screens/home_screen.dart';
import 'screens/chat_screen.dart';
import 'screens/lessons_screen.dart';
import 'screens/quiz_screen.dart';
import 'services/api_service.dart';

Future<void> main() async {
  await dotenv.load(fileName: ".env");
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Provider<ApiService>(
      create: (_) => ApiService(baseUrl: dotenv.env['API_BASE_URL']),
      child: MaterialApp(
        title: 'Smart Shiksha',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF0EA5E9),
            brightness: Brightness.dark,
          ),
          useMaterial3: true,
          scaffoldBackgroundColor: const Color(0xFF121212),
        ),
        home: const HomeScreen(),
        routes: {
          '/home': (context) => const HomeScreen(),
          '/chat': (context) => const ChatScreen(),
          '/lessons': (context) => const LessonsScreen(),
          '/quiz': (context) => const QuizScreen(),
        },
      ),
    );
  }
}
