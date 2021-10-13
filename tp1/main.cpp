#include <iostream>
#include <vector>
#include <cstdlib>
#include <math.h>

using namespace std; 

vector<float>       averages;       //liste des moyennes de one_time_decomp (tmp)

vector<float>       details;        //liste des détails obtenus lors d'une opération de décomposition
//vector<float>       result;         //résultat final renvoyé par une fonction

vector<float>       g_avg;
template<typename T>
void pop_front(std::vector<T>& vec)
{
    if(!vec.empty())
        vec.erase(vec.begin());
}

/* fonction permettant de replacer les détails de la liste de détails dans le bon ordre,
 * pour obtenir le résultat attendu.                                                    
 */ 
vector<float> decomp_reverse(vector<float> v)
{

    vector<float> res;
    int size = v.size();

    /* on retire le dernier pcq la liste sera toujours impaire*/    
    res.push_back(v[size-1]);
    v.pop_back();
    
    if(size>1)
    {
        int i, j;
        do
        {
            //updating the size for each loop
            size = v.size();

            i = size-1;
            j = i - 1;
            res.push_back(v[j]);
            res.push_back(v[i]);
            v.pop_back();
            v.pop_back();
        } while(i>1);
    }
        
    return res;
}
/* TODO: modification de la fonction pour pouvoir faire des n-décompositions */
/* fonction procédant à une étape de décomposition du tableau de flottants donné en argument */
bool one_time_decomp(float* array, int size)
{
    int i = 0;
    int j = 1;
    while(i<size-1)
    {
        averages.push_back( (array[i] + array[j])/2);
        details.push_back( (array[i] - array[j])/2);
        
        i += 2;
        j = i+1;
    }
    return true;
}

void full_decomp(vector<float>& result, vector<float> array, int size)
{
    int i = 0;
    int j = 1;
    
    //tableau averages propre à chaque récursion
    vector<float> avg;
    
    while(i<size-1)
    {
        avg.push_back( (array[i] + array[j])/2);        //average
        details.push_back( (array[i] - array[j])/2);    //detail
        
        i += 2;
        j = i+1;
    }

    //tant qu'on a pas une liste de 2 moyennes, on peut continuer la récursion
    if(size/2 > 1)
    {
        /*float tab[size];
        std::copy(avg.begin(), avg.end(), tab);*/
        for(int i=0; i<size/2; i++)
            avg.push_back(details[i]);
        
        //récursif
        full_decomp(result, avg, size/2);
    }
    //dès qu'on a traité une liste de 2 moyennes, on finit la récursion
    else
    {
        //last average
        result.push_back(avg[0]);
        
        //details sorting
        vector<float> details_new;
        details_new = decomp_reverse(details);
    
        //concatenation finale
        result.insert(result.end(), details_new.begin(), details_new.end());
    }
}

/* fonction de test pour 1 étape de décomposition*/
void course_example()
{

    float tab[4] = {9, 7, 3, 5};
    
    one_time_decomp(tab, 4);
    
    cout << "averages" << endl;
    for(int i=0; i<4/2; i++)
        cout << averages[i] << endl;
        
    cout << "details" << endl;
    for(int i=0; i<4/2; i++)
        cout << details[i] << endl;  
}

/* fonction de test pour l'exemple de décomposition du cours*/
vector<float> course_decomp_full_example()
{
    int size = 256;
    vector<float> tab;
    float t = 0.0;
    float dt = 0.1;

    for(int i=0; i<size; i++)
    {
        tab.push_back((sin(t)/(1.+t)));
        t = t + dt;
    }

    /*tab.push_back(9);
    tab.push_back(7);
    tab.push_back(3);
    tab.push_back(5);*/
    
    vector<float> res;
    cout << "before decomp" << endl;
    full_decomp(res, tab, size);
    cout << "after decomp" << endl;
    return res; 
}

vector<float> one_time_recomp(vector<float> array, int size, int avg_number)
{

    vector<float> avg; //Res
    vector<float> details;
    
   //recuperation des details
   for(int i=avg_number; i<size; i++)
   {
       details.push_back(array[i]);
   }

    int i = 0;
    while (i<avg_number)
    {
        avg.push_back(array[i] + details[i]);
        avg.push_back(array[i] - details[i]);
        
        i += 1;
    }

    for(int i=0; i<avg_number; i++)
        pop_front(details);

    for(int i=0; i<(size-2*avg_number); i++)
    {
        avg.push_back(details[i]);
    }
    
    return avg;
    
}

vector<float> full_recomp(vector<float> array, int size, int avg_number)
{
    int average_number = avg_number;
    vector<float> res;
    
    if(average_number < size)
    {
        res = one_time_recomp(array, size, average_number);
            
        while(average_number < size)
        {
            average_number *= 2;
            if(average_number >= size) break;
            
            res = one_time_recomp(res, size, average_number);
        }
    }
    return res;
}

vector<float> compression(vector<float> array, int size, int epsilon)
{
    //proceeds the decomposition of the values
    vector<float> decomp_res;
    full_decomp(decomp_res, array, size);
    
    float head = decomp_res[0];
    pop_front(decomp_res);
    
    for(int i=0; i<size-1; i++)
    {
        if(abs(decomp_res[i]) < epsilon)
        {
            decomp_res[i] = 0;
        }
    }
    
    vector<float> decomp_compressed;
    decomp_compressed.push_back(head);
    decomp_compressed.insert(decomp_compressed.end(), decomp_res.begin(), decomp_res.end());
    
    vector<float> result;
    result = full_recomp(decomp_compressed, size, 1);
    
    return result;
    
}


int main()
{
    cout << "Début main" << endl;
    vector<float> tab;
    float t = 0.0;
    float dt = 0.1;
    cout << "Début boucle for" << endl;
    for(int i=0; i<256; i++)
    {
        tab.push_back((sin(t)/(1.+t)));
        t = t + dt;

    }
    cout << "avant traitement" << endl;
    for(int i=0; i<256; i++)
    {
        cout << tab[i] << endl;

    }
    //course_example();    
    vector<float> result;
    result = course_decomp_full_example();
    cout << "result:" << endl;
    for(int i=0; i<256; i++)
        cout << result[i] << endl;
        
    vector<float> res;
    res = full_recomp(result, 256, 1);

    for(int i=0; i<256; i++)
    {
        if(tab[i] != res[i])
        {
            cout << "pas ok: " << i << endl;
            break;
        }
        if(i==255)
        {
            cout << "OK" << endl;
        }
    }
    /*cout << "res:" << endl;
    for(int i=0; i<4; i++)
        cout << res[i] << endl;
    */
    /* Compression: 
    - Entry: 9, 7, 3, 5
    
    - epsilon = 4:      6, 6, 6, 6      OK
    - epsilon = 2:      8, 8, 4, 4      OK
    */
    /*vector<float> res_compressed;
    res_compressed = compression(res, 4, 2);
    cout << "compression:" << endl;
    for(int i=0; i<4; i++)
        cout << res_compressed[i] << endl;
    */
    return 0;
}
