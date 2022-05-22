void exeCMD() {
  switch (commands[0]) {
    case 0:
      wdt_disable();
      wdt_enable(WDTO_15MS);
      while (1) {}
      break;

    case 1:
      switch (commands[1]) {
        case 0:
          motorStatus();
          break;
        case 1:
          dirUpdate();
          break;
        case 2:
          setInterval();
          break;
        case 3:
          setMicrosteps();
          break;
        case 4:
          setCurrentLimit();
          break;

        default:
          break;
      }
      break;

    default:
      // statements
      break;
  }
}
