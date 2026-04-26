import { useIsMobile } from '@/hooks/use-mobile';
import PCPoster from '@/pages/PCPoster';
import MobilePoster from '@/pages/MobilePoster';

function App() {
  const isMobile = useIsMobile();

  return isMobile ? <MobilePoster /> : <PCPoster />;
}

export default App;
