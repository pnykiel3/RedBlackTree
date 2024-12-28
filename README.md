# **Drzewa czerwono-czarne**

<br>
<div style="text-align: right"><b>Paweł Nykiel</b></div>

## **1. Wstęp**

Program zrealizowany jako projekt zaliczeniowy z przedmiotu Python.

----------
<br>

## **2. Opis problemu**

Drzewa czerwono-czarne to rodzaj zrównoważonego drzewa binarnego wykorzystywanego w strukturach danych, takich jak mapy czy zbiory. Jest to szczególny przypadek drzewa binarnego poszukiwań, charakteryzujący się dodatkowymi własnościami pozwalającymi na utrzymanie wysokości drzewa w granicach logarytmicznych, nawet w przypadku dużej liczby wstawień i usunięć.
Program implementuje podstawowe operacje na drzewie czerwono-czarnym, takie jak:
1. Wstawianie elementów (z zapewnieniem równowagi drzewa).
2. Usuwanie elementów (z korekcją równowagi drzewa).
3. Przeglądanie drzewa w różnych porządkach (preorder, inorder i postorder).
4. Wizualizacja drzewa w formie graficznej.
5. Walidacja, czy drzewo spełnia właściwości drzewa czerwono-czarnego.

----------
<br>

## **3. Właściwości drzewa czerwono-czarnego**

Drzewa czerwono-czarne zdefiniowane są przez następujące reguły:
1. Każdy węzeł jest albo czerwony, albo czarny.
2. Korzeń drzewa jest zawsze czarny.
3. Czerwony węzeł nie może mieć czerwonych dzieci (brak "czerwonych łańcuchów").
4. Każda ścieżka od korzenia (ROOT) do "pustego liścia" (NULL) zawiera tę samą liczbę czarnych węzłów.

Powyższe reguły pozwalają na utrzymanie logarytmicznej wysokości drzewa i efektywność operacji wstawiania, usuwania i wyszukiwania.

----------
<br>

## **4. Struktura programu**

Aplikacja składa się z dwóch podstawowych klas:
- `Node` (Węzeł): Reprezentuje pojedynczy element drzewa, zawierający wartość, kolor (czerwony lub czarny) oraz wskaźniki na dzieci, rodzica i inne, np. dziadka czy wujka.
- `RBTree` (Drzewo czerwono-czarne): Klasa zarządzająca strukturą drzewa oraz implementująca wszystkie operacje wymagane na tej strukturze.

----------
<br>

## **5. Opis operacji**

Pniższy rozdział zawiera krótkie przedstawienie najistotniejszych operacji wraz z najciekawszymi fragmentami kodu

### **Wstawianie (Insert)**
Wstawianie nowego elementu do drzewa czerwono-czarnego przebiega w dwóch etapach:
1. **Dodanie węzła** zgodnie z metodą wstawiania w drzewie binarnym. Nowy węzeł domyślnie jest czerwony:
``` python
def insert(self, value):
    new = Node(value)
    if self.root is None:  # Jeśli drzewo jest puste, nowy węzeł staje się korzeniem
        self.root = new
        self.root.color = 'black'
    else:
        inserted = self.insert_node(self.root, new)  # Rekurencyjna metoda wstawiania nowego węzła do drzewa BST
        if inserted:
            self.fix_insert(new)  # Naprawa struktury drzewa
```
2. **Naprawa drzewa** po wstawieniu wywoływana jest metoda, która koryguje potencjalne naruszenia reguł drzewa czerwono-czarnego. Wykorzystuje rotacje i zmiany kolorów:
``` python
def fix_insert(self, node):
    while node != self.root and node.parent.color == 'red':
        grandparent = node.grandparent()
        if node.parent == grandparent.left:
            uncle = grandparent.right
            if uncle and uncle.color == 'red':  # Przypadek 1: Wujek jest czerwony
                node.parent.color = 'black'
                uncle.color = 'black'
                grandparent.color = 'red'
                node = grandparent
            else:
                if node == node.parent.right:  # Przypadek 2: Rotacja w lewo
                    node = node.parent
                    self.left_rotate(node)
                node.parent.color = 'black'  # Przypadek 3: Rekolorowanie i rotacja
                grandparent.color = 'red'
                self.right_rotate(grandparent)
        else:
            # Analogiczne przypadki dla rodzica będącego prawym dzieckiem
    self.root.color = 'black'
```

### **Usuwanie (Delete)**
Usunięcie węzła może prowadzić do naruszenia reguł drzewa czerwono-czarnego, w szczególności w przypadku węzłów czarnych. Aby zachować równowagę, stosuje się rekolorowanie i rotacje:
``` python
def delete(self, value):
    node = self.search(value)
    if node is None:
        print(f"Value {value} not found in the tree.")
        return
    self.delete_node(node)
    print(f"Deleted {value} from the tree.")
```
Operacja usuwania obejmuje:
1. Znalezienie węzła do usunięcia.
2. Usunięcie go z drzewa.
3. Naprawę problemów związanych z "podwójną czernią" (double-black), jeżeli trafi ona na ścieżkę po usunięciu węzła.


### **Wczytywanie danych**

```java
/**
* Pobiera od użytownika wielkość grafu 
* i tworzy graf o podanych zależnościach.
*/
private static Graph getGraph() {
  Scanner scanner = new Scanner(System.in);
  int vaultsNumber = scanner.nextInt();
  Graph graph = new Graph(vaultsNumber, false);
```
Na początku tworzę skaner który wczytuje z wejścia standardowego liczbę skarbonek. Tworzę też graf nieskierowany o 
ilości wierzchołków równej ilości skarbonek.

```java
  for (int i = 0; i < vaultsNumber; i++) {
     graph.addEdge(i, scanner.nextInt() - 1);
  }
  return graph;
}
```
Następnie wczytuję krawędzie według schematu opisanego w **Interpretacja problemu**, z modyfikacją polegającą na 
przesunięciu numerówm skarbonek i kluczy aby były od 0 do `n-1` ponieważ tak reprezentowany jest graf.

### **Zliczanie składowych grafu**

```java
/**
 * Zlicza ilość składowych grafu wykorzystując algorytm dfs.
 */
public int countComponents() {
  int numberOfComponents = 0;
  boolean[] visited = new boolean[numberOfVertices];
```
Na początku tworzę tablicę ustawioną na wartość `false` która będzie służyła do oznaczania które wierzchołki już 
odwiedziłem.

```java
  for (int i = 0; i < numberOfVertices; i++) {
    if (!visited[i]) {
        numberOfComponents++;
        dfs1(selectVertex(i), visited);
    }
  }
  return numberOfComponents;
}
```
Następnie przechodzię po kolei przez tablicę i sprawdzam czy któryś wierzchołek nie został jescze odwiedzony. Jeśli 
taki znajdę uruchamiam na nim funkcję przeszukiwania grafu `dfs1`, jednocześnie zwiększając licznik składowych.

### **Przeszukiwanie grafu w głąd (DFS)**

```java
/**
 * Funkcja realizująca algorytm DFS przeglądania grafu.
 */
private void dfs1(Vertex v, boolean[] visited) {
  int vertex = v.Number();
  visited[vertex] = true;
  Iterator<Edge> iterator = EmanatingEdgesIter(vertex);
```
Na początku oznaczam obecny wierzchołek jako odwiedzony i pobieram iterator który zwraca wierzchołki wychodzące z 
danego wierzchołka.

```java
  while (!iterator.isDone()) {
    Vertex x = iterator.getElement().V1();
    if (!visited[x.Number()]) {
      dfs1(x, visited);
    }
    iterator.next();
  }
}
```
Jeśli któryś z wychodzących wierzchołków nie został wcześniej odwiedzony to uruchamiam na nim ponownie algorytm DFS.

----------
<br>

## **6. Opis struktur danych**

Graf jest to struktóra składająca się z wierzchołów i krawędzi które łączą wierzchoki. Jeśli jakieś wierzchołki są 
ze sobą połączone krawędzią to są one sąsiadami.
<br><br>
W rozwiązaniu wykorzystałem graf nieskierowany czyli graf którego krawędzie są dwuelementowymi podzbiorami zbioru 
wierzchołków, czyli upraszczając krawędzie nie mają kierunków.
<br><br>
Grafy możemy reprezentować przy użyciu:
* Macierzy sąsiedztwa
* Listy sąsiedztwa
* Macierzy incydencji

W zadaniu graf z któego korzystałem reprezentowany był z użyciem macierzy sąsiedztwa. Jest to macierz kwadratowa `n` na 
`n`, gdzie `n` jest ilością wierzchołków, w której wartość na przeciąciu `i`-tego wiersza i `j`-tej kolumny 
reprezentuje istnitnie krawędzi miedzy wierzchłkiem `i` oraz `j`.
<br><br>
Do poruszania się po grafie wykorzystywałem wzorzec projektowy iterator który pozwala na sekwencyjne odwiedzanie 
elementów jakiejś większej kolekcji bez potrzeby eksponowania jej formy.

----------
<br>

## **7. Złożoność struktur danych**

### **Złożoność pamięciowa**

Do przechowania `n`-wierzchołkowego grafu z użuciem macierzy sąsiedztwa potrzebujemy tablicę `n` na `n`. W programie 
przechowujemy też `n` wierzchołków więc potrzebujemy tablicy `n` elementowej. Liczby te są stałe więc złożoność 
pamięciowa jest równa O(n^2 + n) = O(n^2).

### **Złożoność czasowa**

1. Utworzenie grafu<br>
   Aby utworzyć graf potrzebujemy utworzyć macierz `n` na `n` i wypełnić ją `null`-ami oraz stworzyć `n` wierzchołków. 
   Złożoność czasowa wynosi więc O(n^2 + n) = O(n^2).
2. Dodanie krawędzi<br>
   Utworzenie krawędzi i wstawienie jej do macierzy sąsiedztwa wykonujemy w czasie stałym. Złożoność czasowa wynosi 
   więc O(1). 
3. Pobranie wierzchołka<br>
   Pobranie wierzchołka wykonujemy w czasie stałym. Złożoność czasowa wynosi więc O(1).
4. Pobranie krawędzi<br>
   Pobranie wierzchołka wykonujemy w czasie stałym. Złożoność czasowa wynosi więc O(1).
5. Wyczyszczenie grafu<br>
   Usunięcie zawartości grafu to przejście przez całą macierz sąsiedztwa i ustawienie w każdej komórce `null`-a. 
   Złożoność czasowa wynosi więc O(n^2).
6. Iterator po wierzchołkach<br>
   Przejście przez wszystkie wierzchołki to przejście przez `n` elementową tablicę. Złożoność czasowa wynosi więc O(n).
7. Iterator po krawędziach wchodzących<br>
   Aby przejść przez wszystkie krawędzie wychodzące wierzchołka trzeba przejść przez całą kolumnę macierzy. Złożoność 
   czasowa wynosi więc O(n).
8. Iterator po krawędziach wychodzących<br>
   Aby przejść przez wszystkie krawędzie wychodzące wierzchołka trzeba przejść przez cały wiersz macierzy. Złożoność czasowa wynosi więc O(n).
9. Iterator po wszystkich krawędziach<br>
   Przejście przez wszystkie krawędzie to przejście przez całą macierz sąsiedztwa. Złożoność czasowa wynosi więc O(n^2).

----------
<br>

## **8. Złożoność algorytmów**

### **Złożoność pamięciowa**

Do działania algorytmu DFS potrzebna jest nam tablica zawierająca `n` pól odpowiadajacych informacji czy dany 
wierzchołek został oznaczony. Liczba ta jest stała więc złożoność pamięciowa jest równa O(n).

### **Złożoność czasowa**

Algorytm DFS potrzebuje przejść przez cały wiersz o długości `n` aby odkryć wszystkie krawędzie wychodzące z 
pojedynczego wierzchołka. Mamy `n` wierzchołków. Złożoność czasowa wynosi więc O(n^2).

----------
<br>

## **9. Sposób uruchomienia**
1. Przejść do katalogu `src`
2. Skompilować kod:<br>
`javac App.java Graph.java Edge.java Vertex.java Iterator.java Visitor.java CountingVisitor.java`<br>
3. Uruchomić program:<br>
`java App`<br>

Następnie podajemy ilość skarbonek. A potem kolejno wpisujemy w której skarbonce znajduje się obecny klucz np.:
```text
Podaj liczbę skarbonek
4
Podaj rozmieszczenie kluczy i skarbonek
2
1
2
4
```

----------
<br>

## **10. Literatura**

https://pl.wikipedia.org/wiki/Spójna_składowa_grafu
<br>
https://pl.wikipedia.org/wiki/Przeszukiwanie_w_głąb
<br>
Slajdy z wykładu i ćwiczeń.

----------
<br>

## **11. Wymagania**

**Java** - testowane na wersji **11**<br>