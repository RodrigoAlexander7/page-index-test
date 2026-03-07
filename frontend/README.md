# Quechua Q&A Frontend

A clean and simple Next.js frontend for interacting with the Quechua Q&A API.

## Features

- **Clean UI**: Simple, intuitive interface for asking questions
- **Real-time Responses**: Get AI-powered answers about Quechua language
- **Source Tracking**: See which document sections were used for answers
- **Responsive Design**: Works on desktop and mobile devices
- **Reusable Components**: Modular component architecture

## Architecture

Built with **KISS principles** and reusable components:

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with metadata
│   ├── page.tsx            # Main Q&A interface
│   └── globals.css         # Global styles
├── components/
│   ├── QuestionInput.tsx   # Input component for questions
│   ├── AnswerCard.tsx      # Display answers with sources
│   ├── SourceCard.tsx      # Show individual sources
│   ├── LoadingSpinner.tsx  # Loading state
│   └── ErrorMessage.tsx    # Error display
└── lib/
    ├── api-client.ts       # API communication
    └── types.ts            # TypeScript types
```

## Tech Stack

- **Next.js 16** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Styling
- **React 19** - UI library

## Setup

### 1. Install Dependencies

```bash
cd frontend
pnpm install
```

### 2. Configure Environment

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
pnpm dev
```

The app will be available at `http://localhost:3000`

## Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm start` - Start production server
- `pnpm lint` - Run ESLint

## Usage

1. **Start the Backend API** first (see backend README)
2. **Start the frontend** with `pnpm dev`
3. **Open** `http://localhost:3000` in your browser
4. **Type a question** about Quechua in the text area
5. **Click "Preguntar"** or press Enter to submit
6. **View the answer** with sources and reasoning

## Component Structure

### QuestionInput
Reusable text input with submit button. Handles:
- Text input
- Enter key submission
- Disabled state during loading

### AnswerCard
Displays API responses with:
- Answer text
- Reasoning/thinking process
- Source documents used

### SourceCard
Shows individual source information:
- Document source (quechua/gramar)
- Title
- Page number

### LoadingSpinner
Simple loading animation during API calls

### ErrorMessage
User-friendly error display with retry option

## API Integration

The frontend communicates with the backend through the `api-client.ts` utility:

```typescript
// Ask a question
const result = await apiClient.askQuestion("¿Cómo se forma el plural?");

// Health check
const health = await apiClient.healthCheck();
```

## Customization

### Colors
Edit Tailwind classes in components to change colors:
- Primary: `blue-600`
- Success: `green-600`
- Error: `red-600`

### API URL
Change in `.env.local`:
```env
NEXT_PUBLIC_API_URL=https://your-api-url.com
```

## Development

The architecture follows KISS principles:
- **Simple**: Minimal complexity, easy to understand
- **Reusable**: Components can be used across the app
- **Maintainable**: Clear separation of concerns
- **Type-safe**: Full TypeScript support

## Production Deployment

### Build the app
```bash
pnpm build
```

### Start production server
```bash
pnpm start
```

### Deploy to Vercel
```bash
vercel deploy
```

Set environment variables in Vercel dashboard:
- `NEXT_PUBLIC_API_URL` - Your production API URL

## License

MIT

