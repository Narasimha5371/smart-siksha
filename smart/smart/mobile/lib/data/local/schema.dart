class SmartShikshaSchema {
  static const int version = 1;

  static const String tableUsers = 'users';
  static const String tableLessons = 'lessons';
  static const String tableProgress = 'student_progress';

  // Table Creation Queries
  static const String createTableUsers = '''
    CREATE TABLE $tableUsers (
      id TEXT PRIMARY KEY,
      username TEXT,
      role TEXT,
      language TEXT,
      last_synced_at TEXT
    )
  ''';

  static const String createTableLessons = '''
    CREATE TABLE $tableLessons (
      id TEXT PRIMARY KEY,
      subject TEXT,
      grade INTEGER,
      title TEXT,
      content_hash TEXT,
      download_url TEXT,
      complexity_level REAL,
      prerequisite_id TEXT,
      local_path TEXT -- For offline file access
    )
  ''';

  static const String createTableProgress = '''
    CREATE TABLE $tableProgress (
      id TEXT PRIMARY KEY,
      student_id TEXT,
      lesson_id TEXT,
      status TEXT,
      score INTEGER,
      attempts INTEGER,
      updated_at TEXT,
      sync_status TEXT -- 'synced', 'dirty'
    )
  ''';
}
