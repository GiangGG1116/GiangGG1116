/**
 * ============================================================================
 * PROFILE CONFIGURATION — CHỈNH SỬA THÔNG TIN CÁ NHÂN TẠI ĐÂY
 * ============================================================================
 * Bạn chỉ cần thay đổi các giá trị trong file này (tên, bio, liên kết,
 * kỹ năng, kinh nghiệm, dự án, GitHub stats...) rồi lưu lại và push lên Git.
 * Không cần sửa code HTML/CSS.
 */
window.PROFILE_DATA = {
  // Tiêu đề tab trình duyệt
  pageTitle: "Trịnh Văn Giang (GiangGG1116) — AI & MLOps Engineer",

  // --------------------------------------------------------------------------
  // 1. SIDEBAR TRÁI (Thông tin cá nhân, liên hệ, Tech Stack, Exploring)
  // --------------------------------------------------------------------------
  sidebar: {
    // Để trống "" để dùng avatar vector mặc định (chỉ dùng 1 ảnh banner nền).
    // Nếu muốn dùng ảnh đại diện thật, hãy điền đường dẫn, ví dụ: "assets/avatar.jpg"
    avatarUrl: "",
    avatarStatusTooltip: "Open to collaborate on AI & MLOps systems",

    name: "Trịnh Văn Giang",
    username: "GiangGG1116",
    headline: "AI Engineer | MLOps Engineer | LLM Systems",
    bio: "Building intelligent systems from Machine Learning models to production-ready AI infrastructure.",

    // Nút hành động chính dưới phần bio (có thể đổi thành Contact Me, Resume, GitHub...)
    actionButton: {
      label: "View GitHub Profile",
      url: "https://github.com/GiangGG1116",
    },

    followers: 2,
    following: 23,

    // Danh sách thông tin liên hệ (icon hỗ trợ: "location", "link", "linkedin", "mail", "github")
    details: [
      {
        icon: "location",
        label: "Hanoi, Vietnam",
        url: "",
      },
      {
        icon: "link",
        label: "https://giangg1.github.io",
        url: "https://giangg1.github.io",
      },
      {
        icon: "linkedin",
        label: "linkedin.com/in/gianggg1116",
        url: "https://www.linkedin.com/in/gianggg1116",
      },
      {
        icon: "mail",
        label: "gianggg1116@gmail.com",
        url: "mailto:gianggg1116@gmail.com",
      },
    ],

    // Tech Stack hiển thị dạng pill ở sidebar trái
    techStackTitle: "Tech Stack",
    techStack: [
      { name: "Python", icon: "python" },
      { name: "PyTorch", icon: "pytorch" },
      { name: "Docker", icon: "docker" },
      { name: "Kubernetes", icon: "kubernetes" },
      { name: "Airflow", icon: "airflow" },
      { name: "MLflow", icon: "mlflow" },
      { name: "KServe", icon: "kserve" },
      { name: "FastAPI", icon: "fastapi" },
      { name: "PostgreSQL", icon: "postgresql" },
      { name: "Qdrant", icon: "qdrant" },
      { name: "MinIO", icon: "minio" },
      { name: "Spark", icon: "spark" },
    ],
  },

  // --------------------------------------------------------------------------
  // 2. BANNER ĐẦU TRANG (Chỉ dùng ảnh nền assets/profile-banner.png)
  // --------------------------------------------------------------------------
  banner: {
    image: "assets/profile-banner.png",
    alt: "Build • Deploy • Scale — AI for a better tomorrow",
    // Ảnh banner hiện tại đã có sẵn chữ. Chỉ bật enabled: true nếu bạn thay
    // bằng ảnh nền phong cảnh chưa có chữ.
    overlayText: {
      enabled: false,
      title: "Build • Deploy • Scale",
      subtitle: "AI for a better tomorrow",
    },
  },

  // --------------------------------------------------------------------------
  // 3. ABOUT ME
  // --------------------------------------------------------------------------
  about: {
    title: "About Me",
    description:
      "I'm an AI Engineer with a background in Mathematics and Informatics, interested in building scalable and production-ready AI systems.",
    // icon hỗ trợ: "graduation", "briefcase", "target", "sparkles"
    highlights: [
      {
        icon: "graduation",
        label: "BSc:",
        value: "Mathematics & Informatics – HUST",
      },
      {
        icon: "graduation",
        label: "MSc:",
        value: "Mathematics & Informatics – HUST (2026–2028)",
      },
      {
        icon: "briefcase",
        label: "Focus:",
        value: "AI Engineering, MLOps, RAG, Agentic AI",
      },
      {
        icon: "target",
        label: "Goal:",
        value: "Design and maintain reliable AI systems",
      },
    ],
  },

  // --------------------------------------------------------------------------
  // 4. CORE EXPERTISE (4 thẻ ngang)
  // --------------------------------------------------------------------------
  expertise: {
    title: "Core Expertise",
    // icon hỗ trợ: "cpu", "chat", "gear", "database", "code", "shield"
    cards: [
      {
        title: "AI & Machine Learning",
        icon: "cpu",
        accentColor: "#38bdf8",
        items: ["Machine Learning", "Deep Learning", "XGBoost, Model Eval"],
      },
      {
        title: "LLM & Agentic AI",
        icon: "chat",
        accentColor: "#60a5fa",
        items: ["RAG, Hybrid Search", "Multi-Agent Systems", "LLM Fine-tuning"],
      },
      {
        title: "MLOps & Infrastructure",
        icon: "gear",
        accentColor: "#7dd3fc",
        items: ["Docker, Kubernetes", "MLflow, Airflow", "KServe, CI/CD"],
      },
      {
        title: "Backend & Data Engineering",
        icon: "database",
        accentColor: "#22d3ee",
        items: ["Python, FastAPI", "SQL, PostgreSQL", "Redis, MinIO / S3"],
      },
    ],
  },

  // --------------------------------------------------------------------------
  // 5. PROFESSIONAL EXPERIENCE (Timeline bên trái)
  // --------------------------------------------------------------------------
  experience: {
    title: "Professional Experience",
    items: [
      {
        role: "FPTS – AI / MLOps Engineer",
        period: "Jul 2026 – Present",
        summary: "ML model deployment, feature engineering, data platform",
      },
      {
        role: "React Plus – AI Engineer",
        period: "Feb 2025 – Jun 2026",
        summary: "RAG, Multi-Agent Systems",
      },
    ],
  },

  // --------------------------------------------------------------------------
  // 6. GITHUB STATS & TOP LANGUAGES
  // --------------------------------------------------------------------------
  stats: {
    title: "GitHub Stats",
    githubUsername: "GiangGG1116",
    // Đặt true nếu muốn tự động lấy % Top Languages từ GitHub API công khai
    // (nếu lỗi mạng hoặc rate limit sẽ tự động dùng dữ liệu tĩnh bên dưới).
    liveLanguagesFromGitHub: false,

    totalContributions: 233,
    contributionLabel: "Total Contributions",
    contributionPeriod: "in the last year",
    months: ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],

    // Ma trận heatmap (5 hàng x 23 cột, giá trị mức độ 0..4).
    // Bạn có thể giữ null để tự động tạo lưới đẹp khớp tổng số contribution,
    // hoặc điền mảng 2 chiều [[0..4], ...] của riêng bạn.
    customHeatmap: null,

    topLanguagesTitle: "Top Languages",
    languages: [
      { name: "Python", percentage: 54.3, color: "#facc15", arcColor: "#facc15" },
      { name: "Go", percentage: 14.2, color: "#38bdf8", arcColor: "#38bdf8" },
      { name: "Other", percentage: 31.5, color: "#475569", arcColor: "#475569" },
    ],
  },

  // --------------------------------------------------------------------------
  // 8. QUOTE CUỐI TRANG
  // --------------------------------------------------------------------------
  quote: {
    text: "“Building AI systems that work beyond the notebook.”",
    emoji: "🚀",
  },
};
